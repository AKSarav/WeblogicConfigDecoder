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
  
  
