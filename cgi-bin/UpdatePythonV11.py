## Update script for AWStats log analyzer and EDG Downloads statistics webpage generation
## Updates current monthly stats webpage daily and current annual stats webpage daily
## Both the monthly and annual config files should both have the same name (internal)

##V1.1 Updates: Change IIS log path from WinServ03 path to WinServ08 path, fix annual folder path output, change perl path to 64 bit

## V1.1 - Jan 2014
## Innovate GIS

#Need to change the path in the monthly config and annual config files to match the CombinedLogFile path used below


import os, subprocess
import time

currentYearMonth = time.strftime("%Y%m")
currentYear = time.strftime("%Y")
currentDay = time.strftime("%d")


#Assign Folder Name using the Current Year and Month
#relative path from where this py script is located
#Need the js and icon folder in this folder as well
staticPagesOutputDir = "./edgdownload/internal/output/simple/" + currentYearMonth
if not os.path.isdir(staticPagesOutputDir):
    print "Creating folder for current month"
    os.makedirs(staticPagesOutputDir)

#Update and combine all one-day log files in logs folder into one large log file to parse.
#relative paths from where this py script is located
with open(os.devnull, "w") as tempFile: 
    subprocess.call(r'C:\perl64\bin\perl.exe logresolvemerge.pl C:\inetpub\logs\LogFiles\W3SVC1\* > ./edgdownload/internal/logs/compositelog/AllLogs.log', shell=True, stdout=tempFile)

#Update the monthly log database
subprocess.call(r"C:\perl64\bin\perl.exe awstats.pl -awstatsprog=D:\Public\Data\DownloadMetrics\cgi-bin\awstats.pl -config=internal -update")

#Update current monthly webpages  
subprocess.call(r"C:\perl64\bin\perl.exe awstats_buildstaticpages.pl -awstatsprog=D:\Public\Data\DownloadMetrics\cgi-bin\awstats.pl -config=internal -update -dir=" + staticPagesOutputDir)

#Switch to annual directory for script execution
os.chdir(r"D:\Public\Data\DownloadMetrics\cgi-bin\annual")
#Update the annual log database
subprocess.call(r"C:\perl64\bin\perl.exe awstats.pl -awstatsprog=D:\Public\Data\DownloadMetrics\cgi-bin\annual\awstats.pl -config=internal -update")
#The annual summarized output HTML is updated
if not os.path.isdir(r"D:\Public\Data\DownloadMetrics\cgi-bin\edgdownload\internal\output\simple" + "\\" + currentYear ):
    os.makedirs(r"D:\Public\Data\DownloadMetrics\cgi-bin\edgdownload\internal\output\simple" + "\\" + currentYear)
subprocess.call(r"C:\perl64\bin\perl.exe awstats_buildstaticpages.pl -awstatsprog=D:\Public\Data\DownloadMetrics\cgi-bin\annual\awstats.pl -config=internal -month=all -year=" + currentYear + r" -update -dir=." + staticPagesOutputDir[:-2])
