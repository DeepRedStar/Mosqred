import os
import subprocess

def generate_self_signed_cert(cert_dir="certs"):
    """Generate a self-signed certificate for local/private deployments."""
    try:
        os.makedirs(cert_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating certificate directory '{cert_dir}': {e}")
        return
    cert_path = os.path.join(cert_dir, "server.crt")
    key_path = os.path.join(cert_dir, "server.key")

    cmd = [
        "openssl", "req", "-x509", "-nodes", "-days", "365", "-newkey", "rsa:2048",
        "-keyout", key_path, "-out", cert_path,
        "-subj", "/CN=localhost"
    ]

    try:
        try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
        return
        print(f"Self-signed certificate created: {cert_path} and {key_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating self-signed certificate: {e}")


def setup_lets_encrypt(domain, cert_dir="/etc/letsencrypt/live"):
    """Use Let's Encrypt to generate trusted SSL certificates for a domain."""
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        try:
        if shutil.which("certbot"):
            print("Certbot is already installed.")
        else:
            subprocess.run(["sudo", "apt-get", "install", "-y", "certbot"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing Certbot: {e}")

        cmd = ["sudo", "certbot", "certonly", "--standalone", "-d", domain]
        subprocess.run(cmd, check=True)

        if not domain or ' ' in domain or '.' not in domain:
        print("Invalid domain provided. Please use a valid domain name.")
        return
    domain_dir = os.path.join(cert_dir, domain)
        if os.path.exists(domain_dir):
            print(f"Let's Encrypt certificate successfully created for domain: {domain}")
        else:
            print(f"Certificate directory for {domain} not found after setup. Check Certbot logs.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up Let's Encrypt certificate for {domain}: {e}")

if __name__ == "__main__":
    # Test self-signed certificate generation
    print("Testing self-signed certificate generation.")
    generate_self_signed_cert()

    # Test Let's Encrypt setup (requires valid domain and network configuration)
    print("Testing Let's Encrypt setup. Replace 'example.com' with your domain.")
    # Uncomment the line below to test with an actual domain
    # setup_lets_encrypt("example.com")
