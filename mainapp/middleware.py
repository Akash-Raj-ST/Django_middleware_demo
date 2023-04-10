from .models import Users
from .cryptography import decrypt

import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import ast

import ast
import random
import os

'''
    The below script is a javascript code which can be run in browser.
    1.  Whenever the form is submitted the default operation is blocked by this code.
        and "submit_form(this)" function is triggered.
    2. Then we extarct the url,public_key,csrf_token from the form fields.
    3. Then for each formdata, we encrypt that using "encrypt(data,public_key)" function.
    4.Then we create new formdata, append all the formdata in it and send the request using fetch.
'''

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
        }).then((response)=>{
                window.location = response.url;
        })
    };
</script>
'''

#this middleware is added in the settings.py

def formProtectionMiddleware(get_response):
    url_path = ""

    #input fields which are hidden and used while encryption
    def fields(url_path,public_key):
        s = f'''
                <input type="hidden" value="{url_path}" name="urlmiddlewaretoken">
                <input type="hidden" value="{public_key}" name="encryptionmiddlewaretoken">
            '''

        return s
    

    #main middleware function
    def middleware(request):

        #Below code executes after the request from client
        #----------------------------------------------

        pwd = os.path.dirname(__file__)

        global url_path

        url_path = request.path
        

        if(request.method=='POST'):
                #list all the params of formdata
                params = list(request.POST)

                id_val = request.session["id_val"]

                #open the file containing private and public keys
                with open(pwd+"/data.txt") as f:
                    data = f.read()
                data = ast.literal_eval(data)

                private_key = data[id_val]['private_key']

                print("POST in middleware:\n")
                print(request.POST)

                request.POST._mutable = True

                #decrypt every formdata value using private key
                for k in params:
                    request.POST[k] = decrypt(private_key, request.POST[k])

                for k in params:
                    print("After decryption inside middleware:\n ",request.POST[k])

                

        response = get_response(request)
        #Below code executes after the response from controller
        #----------------------------------------------

        redirect = 'Location' in response.headers

        #if the response is to redirect don't modify
        if redirect:
            return response
        
        #if the response is of type html perform modification
        if 'html' in response.headers['content-type']:
                
                #generate randome value
                id_val = random.randint(0,4)
                print("random id:",id_val)

                #set the id in the session header
                request.session['id_val'] = id_val

                data = ""

                #fetch the public_key corresponding to id
                with open(pwd+"/data.txt") as f:
                    data = f.read()
                data = ast.literal_eval(data)

                public_key = data[id_val]['public_key']

                print("public_key to send:\n",public_key)
                
                #append custom JS script and the fields in the html response
                response.content += fields(url_path=url_path,public_key=public_key).encode()
                response.content += script.encode()

        return response

    return middleware
