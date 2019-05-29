#!/usr/bin/python
import os
import sys
from sys import argv
from os.path import exists
import re
import time


FLAG = "OFF"
mylist = []
repo = {}
parents = []
servername = ""
ISITWLS8="YES"
valarray=[]
mydict={}
listofservers=[]
stri=" "
serverswls8 = []

# Testing the Startup Arguments for the script
if not (len(argv) > 2 ):
        print "Argument is must"
        sys.exit()

filename = argv[1].rstrip();
hostname = argv[2].strip();
javaversion = argv[3].strip();
domainname = "NULL"
domainversion = "NULL"
servers_out = []
machines_out = []
servertemprepo = []
apps_out = []
toout = []
apps_out_repo = {}

# Environment Variable Setup

if "pl" in hostname:
        Environment = "prod"
elif "ql" in hostname:
        Environment = "qa"
elif "dl" in hostname:
        Environment = "dev"
elif "ul" in hostname:
        Environment = "uat"

founddomain = "false"
founddomainversion = "false"
founddomainv8 = "false"
# Checking if the config.xml file is available to read
if exists(filename):
        #with open(filename,"r+") as fo
        fo = open(filename,"r+")
        os.system("clear")
        print "..Reading the file..",filename
        filecontent = fo.readlines()
        for i, str in enumerate(filecontent):
                matchdomainname = re.search(r'(^\<)(name)(\>)(.+)(\<\/)(name)(\>)', str.strip())
                matchdomainver = re.search(r'(^\<)(domain-version)(\>)(.+)(\<\/)(domain-version)(\>)', str.strip())
                matchdomainv8 = re.search(r'(\<Domain\s)(ConfigurationVersion\=\")([0-9.]*)("\sName\=")([a-z&-_\.]*)(\">)',str.strip())
                if matchdomainname and founddomain == "false":
                        domainname = matchdomainname.group(4)
                        founddomain = "true"
                if matchdomainver and founddomainversion == "false":
                        domainversion = matchdomainver.group(4)
                        founddomainversion = "true"
                if matchdomainv8 and founddomainv8 == "false":
                        ISITWLS8="YES"
                        domainversion = matchdomainv8.group(3)
                        domainname = matchdomainv8.group(5)
                        founddomainv8 = "true"

                if founddomainv8 == "true":
                    match1 = re.search(r'(<Server\s)(.*)', str)
                    if match1:
                        FLAG = "ON"
                        mylist.append(match1.group(2))
                    match3 = re.search(r'^(?!<Server\s)(.*)', str)
                    if match3 and FLAG == "ON":
                        if not "<Server" in match3.group(1):
                            if "ServerVersion" in match3.group(1):
                                mylist.append(match3.group(1).split('>')[0])
                                FLAG = "OFF"
                            else:
                                mylist.append(match3.group(1))
                                FLAG = "ON"
                    match2 = re.search(r'(ServerVersion\=\"[0-9\.-_]*\"\>)', str)
                    if match2:
                        # print str
                        FLAG = "OFF"
                else:
                        ISITWLS8="false"
                        #print " Processing Line: \n",str
                        match1 = re.search(r'\<server\>', str)
                        match1a = re.search(r'\<app-deployment\>',str)
                        if match1 or  match1a:
                            #print str
                            FLAG = "ON"
                        match2 = re.search(r'\<\/server\>', str)
                        match2a = re.search(r'\<\/app-deployment\>',str)
                        if match2 or  match2a:
                            #print str
                            FLAG = "OFF"
                            #print str.strip()
                            mylist.append(str.strip())
                        if (FLAG == "ON"):
                            #print str.strip()
                            mylist.append(str.strip())
                fo.close()
else:
        print "File is not present"
        sys.exit()
##################################################################################################
# HTML
header = '''
<html>
<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Open+Sans|Oxygen" rel="stylesheet">
<link href="https://cdn.datatables.net/1.10.13/css/jquery.dataTables.min.css" rel="stylesheet">
<script type="text/javascript" src="https://code.jquery.com/jquery-3.2.0.min.js"></script>
<script type="text/javascript" src="https://cdn.datatables.net/1.10.13/js/jquery.dataTables.min.js"></script>
<script type="text/javascript" src="/path/to/jquery.tablesorter.js"></script>
<link href="https://fonts.googleapis.com/css?family=Righteous" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Poiret+One" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Overpass" rel="stylesheet">

<script>
   var dataTable = $('.myTable').DataTable();
   var myobj = dataTable.data()

   for (i=0; i<dataTable.data().length;i++)
   {
      console.log(myobj[i].toString());
   }


   var c2 = document.getElementById('consoleaddr').value;
  document.getElementById('consoleurl').innerHTML=c2;

  $("#searchbox").keyup(function(){
        var valuetoapply = $("#searchbox").val();
                dataTable.search( valuetoapply ).draw();
    });

});



</script>
<head>
<style>



html {
 font-family: 'Poiret One', cursive ;
 color: #3d464d;

 background-color: #fff;
 -webkit-font-smoothing: antialiased;
 width: 10s0%;

 overflow: hidden-x;

 /* Centering in The Unknown */
 text-align: center;
}

.dataTables_wrapper .dataTables_length, .dataTables_wrapper .dataTables_filter, .dataTables_wrapper .dataTables_info, .dataTables_wrapper .dataTables_processing, .dataTables_wrapper .dataTables_paginate {
   color: #333;
   font-size: 12px;
}

.datagrid table { border-collapse: collapse; text-align: center; width: 10s0%; } .datagrid { font: normal 10px/150% 'Oxygen', sans-serif;; background: #fff; overflow: hidden; border: 1px solid #8C8C8C; -webkit-border-radius: 3px; -moz-border-radius: 3px; border-radius: 3px; }.datagrid table td, .datagrid table th { padding: 3px 0px; }.datagrid table thead th {background:-webkit-gradient( linear, left top, left bottom, color-stop(0.05, #8C8C8C), color-stop(1, #7D7D7D) );background:-moz-linear-gradient( center top, #8C8C8C 5%, #7D7D7D 100% );filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#8C8C8C', endColorstr='#7D7D7D');background-color:#8C8C8C; color:#FFFFFF; font-size: 15px; font-weight: bold; border-left: 1px solid #A3A3A3; } .datagrid table thead th:first-child { border: none; }.datagrid table tbody td { color: black; border: 1px solid #DBDBDB;font-size: 12px;font-weight: normal; }.datagrid table tbody .alt td { background: #EBEBEB; color: black; }.datagrid table tbody td:first-child { border-left: none; }.datagrid table tbody tr:last-child td { border-bottom: none; }.datagrid table tfoot td div { border-top: 1px solid #8C8C8C;background: #EBEBEB;} .datagrid table tfoot td { padding: 0; font-size: 13px } .datagrid table tfoot td div{ padding: 2px; }.datagrid table tfoot td ul { margin: 0; padding:0; list-style: none; text-align: right; }.datagrid table tfoot  li { display: inline; }.datagrid table tfoot li a { text-decoration: none; display: inline-block;  padding: 2px 8px; margin: 1px;color: #F5F5F5;border: 1px solid #8C8C8C;-webkit-border-radius: 3px; -moz-border-radius: 3px; border-radius: 3px; background:-webkit-gradient( linear, left top, left bottom, color-stop(0.05, #8C8C8C), color-stop(1, #7D7D7D) );background:-moz-linear-gradient( center top, #8C8C8C 5%, #7D7D7D 100% );filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#8C8C8C', endColorstr='#7D7D7D');background-color:#8C8C8C; }.datagrid table tfoot ul.active, .datagrid table tfoot ul a:hover { text-decoration: none;border-color: #7D7D7D; color: #F5F5F5; background: none; background-color:#8C8C8C;}div.dhtmlx_window_active, div.dhx_modal_cover_dv { position: fixed !important; }

body{
display: flex;align-items: center;justify-content: center;
}

.div1
{
padding: 20px;width:600px;height:auto;-webkit-border-radius: 20px;-moz-border-radius: 20px;border-radius: 20px;background-color:;
-webkit-transition: 1s ease-in-out;
        transition: 1s ease-in-out;
        width: 70%;
}


#title
{
font-family: 'Overpass', sans-serif; font-weight: bold;
}


</style>
</head>
<body>


<div class="div1">
<h1 style = "font-family: 'Righteous', cursive;"> CSC Weblogic Inventory  </h1>
<hr>
'''

toout.append(header);

title = '''<hr> <p id="title">DomainName:%s</br>Version:%s</br><strong id="consoleurl">*</strong></p>
<label id="title search">Master Search: <label> <input type="text" name="searchbox" id="searchbox"></input>
<hr>
'''%(domainname,domainversion)

toout.append(title)

##################################################################################################
print "Hostname:%s \n DomainName:%s \n Version:%s"%(hostname,domainname,domainversion)
elements={}

class parent(object):
        def addelement(self,key,value):
                self.__dict__[key]=value


servers=[]
class server(object):
        def addelement(self,key,value):
                self.__dict__[key]=value

# Creating Directory to Place the files
dirname="%s_%s_domain_dumps_%s"%(Environment,domainname,time.strftime('%Y%m%d%H%M%S'))
os.mkdir(dirname)
os.chdir(dirname)

generalfile = "General.properties"
fg = open(generalfile, "w")
appfile=Environment + domainname +"_apps.properties"
csvfile=Environment + domainname +".csv"
fc = open(csvfile,"w")
fapp = open(appfile,"w")
print "I am in "+os.getcwd()+" directory"
mode="parent"
try:
        for line in mylist:
                if ISITWLS8 == "YES":
                    line = line.replace("        ", " ")
                    if "ServerVersion" in line:
                        stri = stri + "  " + line
                        serverswls8.append(stri)
                        stri = ""
                    else:
                        stri = stri + line

                    for entry in serverswls8:
                        entry=entry.strip()
                        #print "WHAT IS AFTER SPLIT",entry.split(" ")
                        valarray.append(entry.split(" "))
                    server8 = {}
                    #print "I AM THE VALARRAY",len(valarray)
                    serverswls8=[]
                    for i in range(len(valarray)):
                        for j in range(len(valarray[i])):
                            # print i,",",j,",",valarray[i][j]

                            match = re.search(r'([a-zA-Z0-9-_\.]*)\=\"([a-zA-Z0-9-_\.]*)\"', valarray[i][j].strip())
                            if match:
                                # server[match.group(1)]=match.group(2)
                                server8[match.group(1)] = match.group(2)
                        #print "WIS", server8
                        listofservers.append(server8.copy())

                        server8.clear()

                    #print "THE WHOLE VALARRAY",valarray
                    # to capture the bogus xml lines <test/>
                if re.search(r'(\<)(.*)(\/)(\>)',line):
                        print "GOT A BOGUS LINE ",line
                        continue
                if re.search(r'(^\<)(.+)(\>)(.+)(\<\/)(.+)(\>)',line):
                        mode="child"
                        match=re.search(r'(^\<)(.+)(\>)(.+)(\<\/)(.+)(\>)',line)
                        if match:
                                if not ( "/" in root ):
                                        var1=root+"_"+match.group(2)
                                        #print "WHAT IS VAR1",var1;
                                        var2=match.group(4)
                                        if ("app-deployment" in var1 ):
                                                writebuffer = var1+":"+var2+"\n";
                                                fapp.write(writebuffer);
                                                apps_out_repo[var1] = var2;
                                                if ("app-deployment_name" in var1 or "app-deployment_source-path" in var1 ):
                                                        apps_out.append(var2);
                                        if var1 == "server_name":
                                                tempvar = '''
<hr>
<p id="title">ServerName : %s</p>
<hr>
<div class="datagrid"><table>
<table class="myTable"><thead><tr><th>Configuration</th><th>Value</th></tr></thead><tbody>
                                           '''%(var2)
                                                toout.append(tempvar)
                                                filename = match.group(4)+".properties"
                                                f = open(filename, 'w')
                                        tempvar1 = '''<tr><td>%s</td><td>%s</td></tr>'''%(var1,var2)
                                        toout.append(tempvar1)
                                        ## THIS IS BEING TAKEN CARE BY DICT PRINT AT THE END print '''%s: %s'''%(var1,var2)
                                        #print root+"_"+match.group(2),":", match.group(4)
                                        elements[root].addelement(root+match.group(2),match.group(4)) #adding new element to the dict
                                        #print elements.keys();
                                        key=root+"_"+match.group(2)
                                        repo[key]=match.group(4)
                                else:
                                        root = root.split("/")[1].strip()
                                        var1 = root + "_" + match.group(2)
                                        var2 = match.group(4)
                                        print var1+":"+var2
                                        tempvar3 = '''<tr><td>%s</td><td>%s</td></tr>'''%(var1, var2)
                                        toout.append(tempvar3)
                                        ## THIS IS BEING TAKEN CARE BY DICT PRINT AT THE END print '''%s: %s'''%(var1, var2)
                                        #print root+"_"+match.group(2),":", match.group(4)
                                        elements[root].addelement(match.group(2),match.group(4)) #adding new element to the dict
                                        key=root+"_"+match.group(2)
                                        repo[key]=match.group(4)



                elif re.search(r'(^\<)(.+)(\>)(\<\/)(.+)(\>)',line):
                        mode="child"
                        match=re.search(r'(^\<)(.+)(\>)(\<\/)(.+)(\>)',line)
                        if match:
                                if not ( "/" in root ):
                                        var1 = root + "_" + match.group(2)
                                        var2 = "NO VALUE"
                                        tempvar4 = '''<tr><td>%s</td><td>%s</td></tr>'''%(var1, var2)
                                        toout.append(tempvar4)
                                        ## THIS IS BEING TAKEN CARE BY DICT PRINT AT THE END print '''%s: %s'''%(var1, var2)
                                        elements[root].addelement(match.group(2),"NO VALUE")
                                        key=root+"_"+match.group(2)
                                        repo[key]="NO VALUE"

                                else:
                                        root = root.split("/")[1].strip()
                                        ## THIS IS BEING TAKEN CARE BY DICT PRINT AT THE END print root+"_"+match.group(2),": NO VALUE"
                                        var1 = root + "_" + match.group(2)
                                        var2 = "NO VALUE"
                                        tempvar5 = '''<tr><td>%s</td><td>%s</td></tr>'''%(var1, var2)
                                        toout.append(tempvar5)
                                        elements[root].addelement(match.group(2),"NO VALUE")
                                        key=root+"_"+match.group(2)
                                        repo[key]="NO VALUE"


                elif re.search(r'(^\<|^\<\/)(.+)(\>$)',line):
                        mode="parent"
                        match=re.search(r'(^\<)(.+)(\>)',line)
                        if match:
                                if not "/" in match.group(2) :
                                        mode = "child"
                                        root=match.group(2)
                                        parents.append(root)
                                else:
                                        root=match.group(2)
                                        mode = "child"
                                        tmpstr=match.group(2).split("/")[1]
                                        if tmpstr in parents:
                                                parents.remove(tmpstr)
                                                if len(parents) > 0:
                                                        root=parents[len(parents)-1]
                        if root not in elements.keys():
                                elements[root] = parent()
                        if root == "/server":
                                endtable = '''
</tbody></table></br></br></div>                                '''
                                toout.append(endtable)
                                #print "Server End:"
                                if "server_name" in repo.keys():
                                        servers.append(repo.copy())
                                        for key, value in repo.copy().iteritems():
                                                whattowrite = key+" = "+value+"\n"
                                                f.write(whattowrite)
                                        repo.clear()
                                        f.close()


except IndexError:
        print "- "
except KeyError:
    print "GotKeyError"

if ISITWLS8 == "YES":
        for serv in listofservers:

                        if 'ListenAddress' in serv.keys():
                                if [ serv['ListenAddress'] == '' ]:
                                        serv['ListenAddress'] = hostname
                                whattowrite=serv['ListenAddress'] + "," + domainname + "," + serv['Name'] + "," + serv['ListenPort'] + "," + domainversion + ","+javaversion+"\n"
                                fc.write(whattowrite)
                        else:
                                whattowrite= hostname + "," + domainname + "," + serv['Name'] + "," + serv['ListenPort'] + "," + domainversion + ","+javaversion+"\n"
                                fc.write(whattowrite)

                        continue


if ISITWLS8 != "YES":
    print "NON WLS8"
    for entry in servers:

            #print CSV Data
            if "server_machine" in entry:
                    machines_out.append(entry['server_machine']) #Add Machine to Dict
                    ttw="\n"+ entry['server_machine'] + "," + domainname + "," + entry['server_name']+ "," +entry['server_listen-port'] +"," +domainversion+","+javaversion
                    fc.write(ttw)
            elif "Admin" in entry['server_name'] and "server_machine" not in entry:
                    ttw="\n"+hostname+","+domainname+","+entry['server_name']+","+entry['server_listen-port']+","+domainversion+","+javaversion
                    fc.write(ttw)
            elif "Admin" in entry['server_name'] and entry['server_listen-address'] != "NO VALUE":
                    ttw="\n"+entry['server_listen-address']+","+domainname+","+entry['server_name']+","+entry['server_listen-port']+","+domainversion+","+javaversion
                    fc.write(ttw)
            if "Admin" in entry['server_name']:
                    #print entry['server_name']+":"+entry['server_listen-port']
                    var1 = "ConsoleURL"
                    var2 = "http://"+hostname+":"+entry['server_listen-port']+"/console"
                    adminurl = '''<input type="hidden" id="consoleaddr" value="%s"></input>'''%(var2)
                    toout.append(adminurl)
                    towrite='''%s = %s'''%(var1, var2)
                    fg.write(towrite)
            else:
                    try:
                            otherurl = '''<input type="hidden" class="serveraddr" value="%s : http://%s:%s, http://%s:%s"></input>'''%(entry['server_name'],entry['server_machine'],entry['server_listen-port'],entry['server_machine'],entry['network-access-point_public-port'])
                            toout.append(otherurl)
                            towrite =  "\n"+entry['server_name']+"_listenerPoints = " + " http://" + entry['server_machine'] + ":" + entry['server_listen-port'] + ", http://" + entry['server_machine'] + ":" + entry['network-access-point_public-port']
                            fg.write(towrite)
                    except KeyError:
                            print "INFO:Got KeyError and Ignored"
            servers_out.append(entry['server_name'])

    finalinfo='''
    <input type="hidden" class="finalinfo" value="Server Instances in this Domain: %s">
    <input type="hidden" class="finalinfo" value="Machines Being used: %s">
    '''%(servers_out,machines_out)
    endhtml = '''

    </div>
    </div>
    </body>
    </html>
    '''
    # HTML OUTPUT WRITE TO FILE
    htmlfilename = Environment + domainname + ".html"
    htmlfilename = htmlfilename.strip()
    fh = open(htmlfilename,'w+')
    toout.append(finalinfo)
    toout.append(endhtml)

    for line in toout:
       fh.write(line)

    fh.close()

generaltowrite='''
DomainName = %s
DomainVersion = %s
Serverinstances = %s
Machines = %s
JavaVersion = %s
Applications = %s'''%(domainname,domainversion,servers_out,machines_out,javaversion,apps_out_repo)


#XLSX REPORTING
fg.write(generaltowrite)
fg.close()
fc.write("\n")
fc.close()
fapp.close()
