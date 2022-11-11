

script = '''<script>
    document.getElementByTagName('form')[0].addEventListener('submit', function(e){
        e.preventDefault();
        submit_form(this);
    })

    function encrypt(data){
        return data+"encrypted";
    }

    function submit_form(e){
        url = "";
        encryption = "";
        
        //whole document
        input_fields = document.getElementByTagName('input');
        for (let i = 0; i < input_fields.length; i++) {
            if(input_fields[i].name == "urlmiddlewaretoken"){
                url = input_fields[i].value;
            }
            if(input_fields[i].name == "encryptionmiddlewaretoken"){
                encryption = input_fields[i].value;
            }
        }

        all_inputs = e.getElementsByTagName('input');
        
        var formData = new FormData(e);
        

        for(var i=0;i<all_inputs.length;i++){
            if(all_inputs[i].type != 'hidden'){
                formData.append(all_inputs[i].name, encrypt(all_inputs[i].value));
                console.log(all_inputs[i].name, encrypt(all_inputs[i].value));
            }
        }
        
        console.log(url, encryption);
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
    };
</script>'''

def formProtectionMiddleware(get_response):
    # One-time configuration and initialization.
    path = ""
    data = ""
    key = "hello"


    def fields():
        global path
        s = f'''
                <input type="hidden" value="{path}" name="urlmiddlewaretoken">
                <input type="hidden" value="{key}" name="encryptionmiddlewaretoken">
            '''

        return s


    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print("Before processing....")
        if(request.path!='/' and request.method=='POST'):

            global path,data
            path = request.path
            data = request.POST
            print(data)
            if 'amount' in data:
                print('amount present')

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        print("After processing...")
        print("path:", path)
        if 'html' in response.headers['content-type']:
            response.content += fields().encode()
            response.content += script.encode()

        
        return response

    return middleware
