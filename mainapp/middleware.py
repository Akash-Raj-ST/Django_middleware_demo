from .models import Users
from .cryptography import decrypt

import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import ast

script = '''<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.2/rollups/aes.js"></script>

<script>
    document.getElementsByTagName('form')[0].addEventListener('submit', function(e){
        e.preventDefault();
        submit_form(this);
    })

    function encrypt(data,public_key,field_name){
        const obj = {public_key:public_key,plain_text:data};

        let headersList = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)",
            "Content-Type": "application/json"
        }

        let bodyContent = JSON.stringify(obj);

        return new Promise((resolve, reject) => {
            fetch("http://127.0.0.1:8000/encrypt/", { 
                method: "POST",
                body: bodyContent,
                headers: headersList
            })
            .then(function(response) {
                    return response.json();
            }).then(function(data) {
                    res = {cipher:data.result,name:field_name};
                    resolve(res);
            })
            }
        )

    }

    async function submit_form(e){
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
        
        var fd = []
        for(var i=0;i<all_inputs.length;i++){
            if(all_inputs[i].type != 'hidden'){

                await encrypt(all_inputs[i].value,public_key,all_inputs[i].name).then(res=>{
                        console.log(res)
                        formData.append(res.name, res.cipher);
                        console.log(res.name, res.cipher)
                        fd[i] = res.name;
                    }
                )
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
                    request.POST[k] = decrypt(rsa_privatekey=private_key, cipher=request.POST[k])

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
