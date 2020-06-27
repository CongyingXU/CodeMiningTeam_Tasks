Metadate：
(20200612) CPE product len: 38634
(20200612) CPE VPwithGitRepo len: 4239
CPE github开源VP中，约400个使用maven构建。



文件说明：
LocalData/
CPE_references.json: CPE中，VP的reference信息合集
CPE_VP.json: CPE中，VP list
VP_GitRepoURL_Map.json: CPE中，从reference中提取，VP与github link的映射

src/
processingCPEDictionary.py: 提取VP list、VP reference信息
mappingVPGitRepo.py: 从VP ref信息中，匹配github url信息，获取VP-GitRepo匹配
