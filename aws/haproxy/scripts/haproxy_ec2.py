from jinja2 import Template
from hashlib import md5
from sys import exit


def search_ec2():
    print "Searching EC2 for servers"
    servers = [
            {'server_ip': '192.168.0.1', 'instance_id': 'i-19216801'},
            {'server_ip': '192.168.0.2', 'instance_id': 'i-19216802'}
    ]

    return servers


def read_file(f):
    try:
        tf = open(f, 'r')
        content = tf.read()
    except IOError as io_error:
        print("Can't open file %s" % f)
        raise(io_error)
    else:
        return content
    finally:
        try:
            tf.close()
        except IOError:
            pass
        
    
def calculate_md5(content):
    return md5(content).hexdigest()


def render_template(content, servers):
    t = Template(content)
    return t.render(servers=servers)


def write_file(content, location):

    try:
        f = open(location, mode='wb')
        f.write(content)
    except IOError as io_error:
        print("Can't write to file %s" % f)
        raise(io_error)


def main():
    try:
        servers = search_ec2()
        haproxy_config = 'haproxy.cfg'
        current_content = read_file(haproxy_config)
        current_md5 = calculate_md5(current_content)

        template = 'haproxy.cfg.j2'
        template_content = read_file(template)
        new_content = render_template(template_content, servers)
        new_md5 = calculate_md5(new_content)

        if new_md5 != current_md5:
            print("Old config doesn't match - writing new content")
            print servers
            write_file(new_content, haproxy_config)
    except Exception as g_exc:
        print g_exc
        print "Not updating the haproxy configuration"
        raise(g_exc)

if __name__ == '__main__':
    exit(main())
