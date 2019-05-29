# WeblogicConfigDecoder
Parse Config.xml file on Remote Weblogic Servers and Create Meaninful Reports


### Step1: Write Your Password into a file named .pwfile ( Not Recommended Need to be modified)

```cat > .passwd```

### Step2: List your remote servers in some file

```
$ cat testfile
testweblogic01
testweblogic02
testweblogic03
```
### Step3: Start the Connect.sh Script and Pass the Properties file

``` ./connect.sh testfile ```



### Step4: Check the reports

in the currently directory check the reports in inventory/<remoteservername>/<domainname>/files
  
  
## List of Files Generated

```
weblogic@testserver> ls -rlt
total 36
-rw-r--r-- 1 weblogic weblogic 11471 May 29 17:04 domainname.html
-rw-r--r-- 1 weblogic weblogic   438 May 29 17:04 domainname.csv
-rw-r--r-- 1 weblogic weblogic   229 May 29 17:04 domainname_apps.properties
-rw-r--r-- 1 weblogic weblogic   596 May 29 17:04 General.properties
-rw-r--r-- 1 weblogic weblogic   944 May 29 17:04 AdminServer.properties
-rw-r--r-- 1 weblogic weblogic  1141 May 29 17:04 ManagedServer2.properties
-rw-r--r-- 1 weblogic weblogic  1111 May 29 17:04 ManagedServer2Server1.properties
```


