## Update script for AWStats log analyzer and EDG Downloads statistics webpage generation
## Updates monthly stats webpage daily and annual stats webpage monthly
## Both the monthly and annual config files should both have the same name (internal)

## V1.0 - Sept 2013
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
    subprocess.call(r'perl logresolvemerge.pl C:\WINDOWS\system32\LogFiles\W3SVC1\* > ./edgdownload/internal/logs/pathToCombinedLogFile/AllLogs.log', shell=True, stdout=tempFile)

#Update the monthly log database
subprocess.call(r"perl awstats.pl -awstatsprog=D:\Public\Data\DownloadMetrics\cgi-bin\awstats.pl -config=internal -update")

#Update current monthly webpages  
subprocess.call(r"perl awstats_buildstaticpages.pl -awstatsprog=D:\Public\Data\DownloadMetrics\cgi-bin\awstats.pl -config=internal -update -dir=" + staticPagesOutputDir)



#On the first of each month, the annual summarized output HTML is updated
if currentDay <> "01":
    if not os.path.isdir(staticPagesOutputDir[:-2]):
        os.makedirs(staticPagesOutputDir[:-2])
    print r"perl annual/awstats_buildstaticpages.pl -awstatsprog=D:\Public\Data\DownloadMetrics\cgi-bin\annual\awstats.pl -config=internal -month=all -year=" + currentYear + r" -update -dir=" + staticPagesOutputDir[:-2]
    subprocess.call(r"perl annual/awstats_buildstaticpages.pl -awstatsprog=D:\Public\Data\DownloadMetrics\cgi-bin\annual\awstats.pl -config=internal -month=all -year=" + currentYear + r" -update -dir=" + staticPagesOutputDir[:-2])
