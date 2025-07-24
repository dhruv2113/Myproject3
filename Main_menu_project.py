import streamlit as st
import paramiko
import psutil

st.title("Unified Operations Menu")

menu = st.sidebar.selectbox(
    "Choose Operation",
    ("Docker SSH Operations", "Linux SSH Operations", "Python Utilities")
)

if menu == "Docker SSH Operations":
    st.header("Remote Docker Control via SSH")
    ip = st.text_input("Remote IP", key="docker_ip")
    username = st.text_input("Username", key="docker_user")
    password = st.text_input("Password", type="password", key="docker_pass")

    if st.button("Connect", key="docker_connect"):
        if not (ip and username and password):
            st.error("Please fill all fields.")
        else:
            st.session_state['docker_ssh'] = None
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username=username, password=password)
                st.session_state['docker_ssh'] = ssh
                st.success("Connected!")
            except Exception as e:
                st.error(f"Connection failed: {e}")

    if 'docker_ssh' in st.session_state and st.session_state['docker_ssh']:
        ssh = st.session_state['docker_ssh']

        st.subheader("Docker Commands")

        if st.button("List Containers"):
            stdin, stdout, stderr = ssh.exec_command("docker ps -a")
            st.code(stdout.read().decode() + stderr.read().decode())

        if st.button("List Images"):
            stdin, stdout, stderr = ssh.exec_command("docker images")
            st.code(stdout.read().decode() + stderr.read().decode())

        container_name = st.text_input("Container Name")
        image_name = st.text_input("Image Name (for launch)")

        if st.button("Launch New Container"):
            if container_name and image_name:
                cmd = f"docker run -dit --name={container_name} {image_name}"
                stdin, stdout, stderr = ssh.exec_command(cmd)
                st.code(stdout.read().decode() + stderr.read().decode())
            else:
                st.warning("Enter both container name and image name.")

        if st.button("Start Container"):
            if container_name:
                cmd = f"docker start {container_name}"
                stdin, stdout, stderr = ssh.exec_command(cmd)
                st.code(stdout.read().decode() + stderr.read().decode())
            else:
                st.warning("Enter container name.")

        if st.button("Stop Container"):
            if container_name:
                cmd = f"docker stop {container_name}"
                stdin, stdout, stderr = ssh.exec_command(cmd)
                st.code(stdout.read().decode() + stderr.read().decode())
            else:
                st.warning("Enter container name.")

        if st.button("Remove Container"):
            if container_name:
                cmd = f"docker rm -f {container_name}"
                stdin, stdout, stderr = ssh.exec_command(cmd)
                st.code(stdout.read().decode() + stderr.read().decode())
            else:
                st.warning("Enter container name.")

        if st.button("Disconnect"):
            ssh.close()
            st.session_state['docker_ssh'] = None
            st.success("Disconnected.")

elif menu == "Linux SSH Operations":
    st.header("Remote Linux Control via SSH")
    ip = st.text_input("Remote IP", key="linux_ip")
    username = st.text_input("Username", key="linux_user")
    password = st.text_input("Password", type="password", key="linux_pass")

    if st.button("Connect", key="linux_connect"):
        if not (ip and username and password):
            st.error("Please fill all fields.")
        else:
            st.session_state['linux_ssh'] = None
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username=username, password=password)
                st.session_state['linux_ssh'] = ssh
                st.success("Connected!")
            except Exception as e:
                st.error(f"Connection failed: {e}")

    if 'linux_ssh' in st.session_state and st.session_state['linux_ssh']:
        ssh = st.session_state['linux_ssh']
        st.subheader("Linux Commands")
        if st.button("List Files (ls -l)"):
            stdin, stdout, stderr = ssh.exec_command("ls -l")
            st.code(stdout.read().decode() + stderr.read().decode())
        if st.button("Show Current Directory (pwd)"):
            stdin, stdout, stderr = ssh.exec_command("pwd")
            st.code(stdout.read().decode() + stderr.read().decode())
        if st.button("Show Disk Usage (df -h)"):
            stdin, stdout, stderr = ssh.exec_command("df -h")
            st.code(stdout.read().decode() + stderr.read().decode())
        if st.button("Show Memory Usage (free -m)"):
            stdin, stdout, stderr = ssh.exec_command("free -m")
            st.code(stdout.read().decode() + stderr.read().decode())
        if st.button("Show Uptime"):
            stdin, stdout, stderr = ssh.exec_command("uptime")
            st.code(stdout.read().decode() + stderr.read().decode())
        if st.button("Show Running Processes (ps aux)"):
            stdin, stdout, stderr = ssh.exec_command("ps aux")
            st.code(stdout.read().decode() + stderr.read().decode())
        if st.button("Disconnect", key="linux_disconnect"):
            ssh.close()
            st.session_state['linux_ssh'] = None
            st.success("Disconnected.")

elif menu == "Python Utilities":
    st.header("Python Utilities")

    # RAM Usage
    if st.button("Show RAM Usage"):
        ram = psutil.virtual_memory()
        st.write(f"RAM Usage: {ram.percent}% | Available: {round(ram.available / 1e9, 2)} GB | Total: {round(ram.total / 1e9, 2)} GB")

    # Post a Tweet
    if st.button("Post a Tweet"):
        with st.form("tweet_form"):
            tweet_api_key = st.text_input("Twitter API Key")
            tweet_api_secret = st.text_input("Twitter API Secret")
            tweet_access_token = st.text_input("Twitter Access Token")
            tweet_access_token_secret = st.text_input("Twitter Access Token Secret")
            tweet_text = st.text_input("Tweet Text")
            submit_tweet = st.form_submit_button("Send Tweet")
            if submit_tweet:
                try:
                    import tweepy
                    auth = tweepy.OAuth1UserHandler(tweet_api_key, tweet_api_secret, tweet_access_token, tweet_access_token_secret)
                    api = tweepy.API(auth)
                    api.update_status(tweet_text)
                    st.success("Tweet posted successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Send SMS via Twilio
    if st.button("Send SMS via Twilio"):
        with st.form("twilio_form"):
            twilio_sid = st.text_input("Twilio Account SID")
            twilio_token = st.text_input("Twilio Auth Token")
            twilio_from = st.text_input("Twilio From Number")
            twilio_to = st.text_input("Destination Number")
            twilio_msg = st.text_input("Message")
            submit_sms = st.form_submit_button("Send SMS")
            if submit_sms:
                try:
                    from twilio.rest import Client
                    client = Client(twilio_sid, twilio_token)
                    message = client.messages.create(body=twilio_msg, from_=twilio_from, to=twilio_to)
                    st.success(f"Message sent! SID: {message.sid}")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Post to LinkedIn
    if st.button("Post to LinkedIn"):
        with st.form("linkedin_form"):
            linkedin_token = st.text_input("LinkedIn Access Token")
            linkedin_person_id = st.text_input("LinkedIn Person ID")
            linkedin_text = st.text_input("Post Text")
            submit_linkedin = st.form_submit_button("Post to LinkedIn")
            if submit_linkedin:
                import requests
                import json
                def create_post_data(text):
                    return {
                        "author": f"urn:li:person:{linkedin_person_id}",
                        "lifecycleState": "PUBLISHED",
                        "specificContent": {
                            "com.linkedin.ugc.Post": {
                                "shareMediaCategory": "ARTICLE",
                                "text": {"text": text}
                            }
                        },
                        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
                    }
                url = "https://api.linkedin.com/v2/ugcPosts"
                headers = {
                    "Authorization": f"Bearer {linkedin_token}",
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0"
                }
                post_data = create_post_data(linkedin_text)
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(post_data))
                    if response.status_code == 201:
                        st.success("Post created successfully!")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Exception occurred: {e}")

    # Create and save a simple image
    if st.button("Create and Save a Simple Image"):
        with st.form("image_form"):
            submit_image = st.form_submit_button("Create Image")
            if submit_image:
                try:
                    from PIL import Image, ImageDraw, ImageFont
                    width, height = 400, 300
                    background_color = (30, 30, 30)
                    img = Image.new("RGB", (width, height), background_color)
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([(50, 50), (350, 120)], fill=(0, 102, 204))
                    draw.ellipse([(150, 150), (250, 250)], fill=(255, 0, 0))
                    font = ImageFont.load_default()
                    draw.text((60, 60), "Hello, Digital World!", fill=(255, 255, 255), font=font)
                    img.save("my_digital_art.png")
                    st.image(img, caption="Digital Art")
                    st.success("Image saved as 'my_digital_art.png'")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Tuple vs List memory/speed/mutability/hashability
    if st.button("Tuple vs List: Memory, Speed, Mutability, Hashability"):
        with st.form("tuple_list_form"):
            submit_tuple_list = st.form_submit_button("Show Tuple vs List Comparison")
            if submit_tuple_list:
                import sys
                import time
                my_tuple = (1, 2, 3, 4, 5)
                my_list = [1, 2, 3, 4, 5]
                mem_tuple = sys.getsizeof(my_tuple)
                mem_list = sys.getsizeof(my_list)
                start_tuple = time.time()
                for _ in range(1000000):
                    for item in my_tuple:
                        pass
                end_tuple = time.time()
                start_list = time.time()
                for _ in range(1000000):
                    for item in my_list:
                        pass
                end_list = time.time()
                mutability = "Tuple: ❌ Cannot modify – it’s immutable\nList : ✅ Can modify – it’s mutable"
                try:
                    hash(my_tuple)
                    hash_tuple = "Tuple: ✅ Hashable – usable as dictionary key"
                except TypeError:
                    hash_tuple = "Tuple: ❌ Not hashable"
                try:
                    hash(my_list)
                    hash_list = "List : ✅ Hashable"
                except TypeError:
                    hash_list = "List : ❌ Not hashable – cannot be a dictionary key"
                st.write(f"🔍 Memory size (bytes): Tuple: {mem_tuple}, List: {mem_list}")
                st.write(f"⚡ Speed test (1M iterations): Tuple: {end_tuple - start_tuple:.5f} s, List: {end_list - start_list:.5f} s")
                st.write(mutability)
                st.write(hash_tuple)
                st.write(hash_list)

    st.info("Add more Python utilities here as needed.") 
