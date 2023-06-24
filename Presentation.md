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
