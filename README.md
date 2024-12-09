# OR-LLM
Create mathematical optimization models and code using LLM's!

## Overview
This web application is for formulating and coding  Mixed Integer and Linear Problems with the use of a Large Language Model. 
![alt text](https://github.com/retrorecon/or-llm/blob/main/or-llm-sample-usage.png?raw=true)

## Features
The chat window is intended for discussing back and forth with an LLM agent. As the user explains their problem, the agent creates appropriate MILP model formulations. 

The agent can also provide Python code with using the library PuLP as an open-source optimizer.

The agent stores chat history during a conversation, and can provide adjustments to both the mathematical model and to the code. Simply ask for changes!
Although, the chat history will be deleted after the user leaves the website or the service is terminated.

## Install
Simply install the required libraries with the `requirements.txt` file.
```sh
pip install -r requirements.txt
```
## Usage
After locating into the project directory, you can launch the locally hosted server as following.
```sh
streamlit run st_app.py
```
Alternatively you can also use Python module to launch the service.
```sh
python -m streamlit run st_app.py
```

## Capabilities
The user can interact with the agent as a regular chatbot, but the coding block shown in the layout will be only used for code translation of the mathematical model. Hence, if a user requests to code something else, it will not be visible in that pane, but in the regular chat.

Message streaming is not available for now, as the interaction with the model takes place in a JSON format. Streaming can be implemented in the future.

After creating a mathematical model, if the user tries to talk about different topics not related to the model, the LLM agent can sometimes ignore the user. This behavior changes based upon the prompt given in the source code, so you can try out different things yourself!

## Maintainers
Emir Demirbilek [@retrorecon](https://github.com/retrorecon).

## License

[MIT](LICENSE) © Emir Demirbilek
