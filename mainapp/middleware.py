from .models import Users
from .cryptography import decrypt

import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import ast

script = '''
<script src="https://cdnjs.cloudflare.com/ajax/libs/jsencrypt/2.3.1/jsencrypt.min.js"></script>

<script>
    document.getElementsByTagName('form')[0].addEventListener('submit', function(e){
        e.preventDefault();
        submit_form(this);
    })

    function encrypt(data,public_key){    
        const encrypt = new JSEncrypt();
        encrypt.setPublicKey(public_key);
        const result = encrypt.encrypt(data);
        return result;
    }

    function submit_form(e){
        console.log("submit using manual...");

        url = "";
        public_key = "";
        csrf_value = "";

        //whole document
        input_fields = document.getElementsByTagName('input');

        for (let i = 0; i < input_fields.length; i++) {
            if(input_fields[i].name == "urlmiddlewaretoken"){
                url = input_fields[i].value;
            }
            else if(input_fields[i].name == "encryptionmiddlewaretoken"){
                public_key = input_fields[i].value;
            }
            else if(input_fields[i].name == "csrfmiddlewaretoken"){
                csrf_value = input_fields[i].value;
            }
        }

        all_inputs = e.getElementsByTagName('input');
        
        var formData = new FormData();
        
        for(var i=0;i<all_inputs.length;i++){
            if(all_inputs[i].type != 'hidden'){

                const encrypt_value = encrypt(all_inputs[i].value,public_key);

                formData.append(all_inputs[i].name, encrypt_value);
                console.log(all_inputs[i].name, encrypt_value)
                    
            }
        }

        for (var pair of formData.entries()) {
            console.log(pair[0]+ ' - ' + pair[1]); 
        }

        //sending encrypted data
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrf_value
            }
        })
    };
</script>
    
    
'''

def formProtectionMiddleware(get_response):
    # One-time configuration and initialization.
    url_path = ""

    def fields(url_path,public_key):
        s = f'''
                <input type="hidden" value="{url_path}" name="urlmiddlewaretoken">
                <input type="hidden" value="{public_key}" name="encryptionmiddlewaretoken">
            '''

        return s

    def middleware(request):
       
        global url_path

        if(request.path!='/'):
            url_path = request.path
            
            if(request.method=='POST'):
                params = list(request.POST)

                user = Users.objects.get(user_id=request.session['user_id'])
                private_key = user.private_key
                print("POST:")
                print(request.POST)

                request.POST._mutable = True
                for k in params:
                    request.POST[k] = decrypt(private_key, request.POST[k])

                for k in params:
                    print("After decryption: ",request.POST[k])
                

        response = get_response(request)
        #----------------------------------------------

        print(request.path)
        if request.path != '/' and request.path != '/favicon.ico':
            if 'html' in response.headers['content-type']:
                print("user id:",request.session['user_id'])
                user = Users.objects.get(user_id=request.session['user_id'])
                public_key = user.public_key
                response.content += fields(url_path=url_path,public_key=public_key).encode()
                response.content += script.encode()

        
        return response

    return middleware
