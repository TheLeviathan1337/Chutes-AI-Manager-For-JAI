# Chutes-AI-Manager-For-JAI

Welcome! This repository was a personal thing I created for myself to improve my Quality of Life when using Chutes AI for JanitorAI. I wanted two problems solved that really annoyed me,

1. The reasoning tokens for models with reasoning tokens would always be sent back into the chat, meaning I would either have to bloat the chat with reason tokens or manually delete them every time. It also meant that I would "Spoil" myself and see a sneak-peek of what was to come, this annoyed me and I wanted a solution to fix this.

2. Sometimes, I noticed that using only one model could feel like it's not as fresh, maybe 1 model would always get stuck on something. Maybe 1 Model just simply struggled to respond to one message in particular. So I wanted a way to incorporate multi-model support into my responses.

---
# The Solution

Here comes the solution! A very small and simple FastAPI server that runs as a middle man as your proxy, specifically designed to handle Chutes AI requests. It essentially *becomes* your proxy in a way. It fixes both of the problems above, it removes reasoning tokens from your responses, and it lets you create a configuration to use multiple models at once using two possible modes!

1. Random: Each time you send a response requesting an LLM response (For a new message or a re-try or really anything), it randomly picks from your configured models

2. Ordered: The model predictably follows a turn order (i.e. Model 1, Model 2, Model 3 and then repeat) to constantly shift and change what model it uses.

---
# Running the Server

This project was written in Python 3.12.10. You will first, naturally, need to have Python3 on your system (Not entirely sure how far backwards compatible it is), the pip package installer, and you will need to either clone this project onto your computer or download the files into its own folder. Once you have python and the project files, we first need to install the dependencies of the program.

In whatever python environment you use, run the `pip install -r requirements.txt` command (or whatever equivalent you need to invoke pip) to install all the required packages and modules for this simple middleman server, of course, as the command implies they are located in the requirements.txt file included with the project files.

Next, let's initialize our .env, in the project files for the code there is a file called ".env.example", you should COPY this file and duplicate it in your project folder and rename it to ".env". Upon doing so, you should see something like this:

![image](https://github.com/user-attachments/assets/f09f9cb9-03e1-4130-8b4b-737eb2053951)

There are two environment variables we need to resolve. 

Immediately after the CHUTES_API_KEY= put your Chutes API key.

Do not include any spaces or quotation marks, it should look something like CHUTES_API_KEY=cpk_abunchofnumbers

You will no longer need to put your API key into Janitor AI's GUI because we are just going to load it locally on our middleman server and use it every time there, which I included for myself as a quality of life feature because I didn't want to go fetch my api key every time.

Second, immediately after PORT_NUMBER= just choose some arbitrary port number. If you cant decide, 6969 should work, this will just determine what port your middleman server will run on.

Next, let's take a look at the model_configs.py file.

![image](https://github.com/user-attachments/assets/37a145c8-b557-42bc-89b3-a496a21e64e1)

You can edit this file to your heart's content. In each class, you should add information for new Chutes models, and the kind of temperatures and other settings you would prefer them to have. This file has comment instructions to guide you, so it should be fairly straight forward. I will say though, the reasoning start_reasoning_tokens can be a hassle is because of Deepseek R1T Chimera. It, extremely annoyingly, doesn't actually have a start <think> value when its reasoning tokens begin like Deepseek R1 has. And it sometimes doesn't return reasoning tokens at all. I have noticed that it tends to either start its reasoning with "Okay, " or "Alright" so I have chosen to utilize those. IF YOU NOTICE OTHER POSSIBLE BEHAVIOR, FEEL FREE TO EDIT THIS LIST TO INCLUDE NEW POSSIBLE TOKENS!

EDIT: I have already encountered issues with this and have moved the "Okay, " to just an "Okay" so expect to see it a bit different in your file as the screenshot, but that is a good thing

V3 and R1 behave pretty much as expected because V3 has no reasoning tokens and R1 always starts with <think> and ends with </think>, so there's simply no problem.

By default, I have initialized all 3 of the most popular Deepseek models for Janitor AI as being included and active with a random basic configuration. Feel free to finetune to your hearts content! Do you like V3 on high temp and R1 on low temp? You can have both! Edit your models individually how you please, and add more models according to the instructions in the example, you can add whatever Chutes model you want :)

Now, to run the server, just simply run

`python main.py`

---
# Setting up the Proxy on JanitorAI

![image](https://github.com/user-attachments/assets/b2a9d09e-20e6-41ae-83ac-9af80c3e6945)

Lets turn our attention to the basic JanitorAI proxy settings. These are the settings we will be using to use our middleman program.

NOTE: ALWAYS REFRESH YOUR PAGE AFTER UPDATING PROXY SETTINGS OR THEY WONT WORK!

First, we will put literally anything into the API key and Model section. We literally won't make use of them, but Janitor AI gets angry when you leave them empty, so just put literally anything in them.

So now it should look something like this:

![image](https://github.com/user-attachments/assets/486ad918-d30b-4dd1-a92e-06344fa9b0da)

Next thing we will do is define the url. We have two possible choices!

1. The Easy Choice: You are using JanitorAI on the same PC you are running your server on. In which case, you can begin by typing http://localhost:PORT_NUMBER/proxy/ just like so in the following example below:

![image](https://github.com/user-attachments/assets/54e5c3e5-f57c-4cc8-8cda-124aacad5d4a)

2. The Harder (But not Insanely Harder Choice): You are using JanitorAI on a different device than you are running your server on (Like your phone)

If this is the case, then you need to use some sort of service to create a public-facing IP address to put here. One such method is to use ngrok which can be downloaded here: https://ngrok.com/

Once you have configured ngrok and it is running (Or some other service) You can type something like the_public_facing_link_they_gave_you/proxy/

Now you have TWO options as endpoints, you can add "random" to utilize random LLM switching and you can add "ordered" to utilize ordered LLM switching, like the examples below in finality:

Here are some examples below using localhost:

![image](https://github.com/user-attachments/assets/72fbb7ae-0ec6-4b95-ae60-c91f7840b3d4)
![image](https://github.com/user-attachments/assets/971e9a70-02e8-489b-8b1c-2580722bc0d3)

From there? You should be completely okay to just save, refresh your page, and have fun, it should all be working completely! :D

# NOTICE:

Yes I know I'm using github file upload, I swear I don't have skill issues I just CBA to either post this on one of my actual github accounts or to create new RSA credentials for this account, and the project is too small for me to GAF about git, so this is what you "git"! 

