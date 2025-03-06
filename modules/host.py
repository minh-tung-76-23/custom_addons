import subprocess

def run_odoo():
    list_process = ['lsof', '-i', 'tcp:8069']
    result = subprocess.run(list_process, capture_output=True, text=True)
    # print(result)
    for line in result.stdout.splitlines():
        if 'Python' in line:
            pid = int(line.split()[1])
            # print(pid)
            subprocess.run(['kill','-9', str(pid)])

    start_server = ['/Users/mac/Dev/Intern/Python/odoo/odoo-bin', '-c', '/Users/mac/Dev/Intern/Python/odoo/odoo.conf']
    subprocess.run(start_server)

if __name__ == "__main__":
    run_odoo()