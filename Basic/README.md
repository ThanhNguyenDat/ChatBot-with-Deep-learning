# ChatBot-with-Deep-learning-Basic

## Dialog Systems in Detail

The main idea of a dialog system or chatbot is to understand a user’s query or input and to provide an appropriate response. This is different from typical questionanswering systems where, given a question, there has to be an answer. In a dialog setup, users may ask their queries in “turns.” In each turn, a user reveals their interest about the topic based on what the bot may have responded with. So, in a dialog system, the most important thing is understanding nuances from the user’s input in a turn-by-turn way and storing them in context to generate responses.

Before we get into the details of bots and dialog systems, we’ll cover the terminology used in dialog systems and chatbot development more broadly.

#### Dialog act or intent

This is the aim of a user command. In traditional systems, the intent is a primary descriptor. Often, several other things, such as sentiment, can be linked to the intent. The intent is also called a “dialog act” in some literature. In the first example in Figure 6-4, orderPizza is the intent of the user command. Similarly, in the second example, the user wants to know about a stock, so the intent is getStock‐Quote. These intents are usually pre-defined based on the chatbot’s domain of operation.

#### Slot or entity

This is the fixed ontological construct that holds information regarding specific entities related to the intent. The information related to each slot that’s surfaced
in the original utterance is “value.” The slots and value together are sometimes denoted as an “entity.” Figure 6-4 shows two examples of entities. The first example looks for specific attributes of the pizza to be ordered: “medium” and “extra cheese.” On the other hand, the second example looks for the related entities for
getStockQuote: the stock name and the time period the chatbot is asked for.

#### Dialog state or context

A dialog state is an ontological construct that contains both the information about the dialog act as well as state-value pairs. Similarly, context can be viewed as a set of dialog states that also captures previous dialog states as history.

![image](https://user-images.githubusercontent.com/76576719/128008205-2e4ba706-5686-43b3-ba54-08f80accdbf6.png)
