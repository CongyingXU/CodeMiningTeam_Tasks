### RiskDB 构建数据流程

> 目前，以common-cli为case，已将整个流程跑通！

1. 爬取issue info

   > RiskDB/Crawler/JIRA_Crawling.py 

2. 将issue部分数据导入sqlite DB

   >  RiskDB/Crawler/ImportDBissues.py

3. Map issueKey-CommitID

   > /LibDetectRec/RiskDB/CommitExtractor/BuggyMethodsExtraction/src/main/java/cn/edu/fudan/se/buggymethod/SearchCommitIdFromRepo.java

4. 生成 batch文件

   > GenBatchCmds.java

5. Extract buggymethod based on commitID

   > ExtractBuggyMethods.java

6. 将buggyMethod数据按照每个issue进行整合  

   > FormatBuggyMethods.java