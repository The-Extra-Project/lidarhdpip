# bootstrap.servers="pkc-xrnwx.asia-south2.gcp.confluent.cloud:9092"
# security.protocol=SASL_SSL
# sasl.mechanisms=PLAIN


def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf


