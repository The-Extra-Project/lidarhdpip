[![](https://mermaid.ink/img/pako:eNqVk01vAiEQhv8K4Vpr0isHD42emiamay_NXsZldIm7QIfBaoz_vdDVuGps65z4eJn3GWB2snIapZIBPyPaCscGlgRtaUUKDySm5CoMQbxlQeBuI8fsyzAjvQekx9HoMHt2rI5S8XSPeDgc3iO3nRisFlOgYOxS0CVh45wXkzXSVmxEa2zkcNrM8QKLFRRIa1Nh8nnoG-WseF01Wn1yHpvAZOaRUYvKtT4ysHH2gmBWE4IW3rnmd_s5VNDUENXtSz-zn2y8I-5KD7Hh__oefZJnr4IMgqTEGH3jtsk6pww3T_bhlSgS2BXFGew0zhsT6hNtL_XFRZy_d9b2v9Lf4sMDZCQ5kC1SC0anP77L66XkGlsspUpDDbQqZWn3SQeRXbG1lVRMEQcyeg187AepFtCEtIrasKPXrml-emcgPdgP59ru4P4bY0YSug?type=png)](https://mermaid.live/edit#pako:eNqVk01vAiEQhv8K4Vpr0isHD42emiamay_NXsZldIm7QIfBaoz_vdDVuGps65z4eJn3GWB2snIapZIBPyPaCscGlgRtaUUKDySm5CoMQbxlQeBuI8fsyzAjvQekx9HoMHt2rI5S8XSPeDgc3iO3nRisFlOgYOxS0CVh45wXkzXSVmxEa2zkcNrM8QKLFRRIa1Nh8nnoG-WseF01Wn1yHpvAZOaRUYvKtT4ysHH2gmBWE4IW3rnmd_s5VNDUENXtSz-zn2y8I-5KD7Hh__oefZJnr4IMgqTEGH3jtsk6pww3T_bhlSgS2BXFGew0zhsT6hNtL_XFRZy_d9b2v9Lf4sMDZCQ5kC1SC0anP77L66XkGlsspUpDDbQqZWn3SQeRXbG1lVRMEQcyeg187AepFtCEtIrasKPXrml-emcgPdgP59ru4P4bY0YSug)


```mermaid
---
Sequence Diag
---
sequenceDiagram
    par Process Request
        TwitterUser->>TwitterBot: Request 1
        TwitterUser->>TwitterBot: Request ...
        TwitterUser->>TwitterBot: Request n
    and Parsing request
        loop Every x minuts
            KafkaService->>+TwitterBot: Parse Request
        end
    and Distributed computation
        loop Thread pool
            KafkaService->>+bacalhau: Process Request
        end
    and Exporting result
        loop Thread pool
            bacalhau->>DistributedServer: Deploy Results
            bacalhau->>KafkaService: Send result
        end
    and Publishing results
        KafkaService->>TwitterBot: Result 1
        KafkaService->>TwitterBot: Result n
    end 
    sequenceDiagram
    par Process Request
        TwitterUser->>TwitterBot: Request 1
        TwitterUser->>TwitterBot: Request ...
        TwitterUser->>TwitterBot: Request n
    and Parsing request
        loop Every x minuts
            KafkaService->>+TwitterBot: Parse Request
        end
    and Distributed computation
        loop Thread pool
            KafkaService->>+bacalhau: Process Request
        end
    and Exporting result
        loop Thread pool
            bacalhau->>DistributedServer: Deploy Results
            bacalhau->>KafkaService: Send result
        end
    and Publishing results
        KafkaService->>TwitterBot: Result 1
        KafkaService->>TwitterBot: Result n
    end 
```
