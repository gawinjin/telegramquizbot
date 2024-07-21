Telegram Quiz Bot

A Telegram bot that conducts interactive quizzes. This bot allows authorized users to initiate quiz sessions, while enabling open participation for all chat members. It's designed to engage users with questions about SOFA.org, its features, and its ecosystem.

Features

- Restricted quiz initiation: Only authorized users can start quiz sessions
- Open participation: All chat members can answer quiz questions
- Customizable quiz sessions: Adjust the number of questions and duration
- Timed quiz sessions: Questions are sent at regular intervals
- Automatic score tracking and result summary
- Customizable question pool with 40+ pre-defined questions about SOFA.org
- Error handling and question validation

Requirements

- pyTelegramBotAPI

To find the chat ID:

1. Add your bot to the desired group chat.
2. Send a message in the group chat.
3. Open this URL in your browser, replacing `<BOT_TOKEN>` with your actual bot token:

   https://api.telegram.org/bot<BOT_TOKEN>/getUpdates

4. Look for the `"chat":{"id":` field in the response. The number after it is your chat ID.
5. If the chat ID is positive, it's a private chat. If it's negative, it's a group chat.

Note: For privacy reasons, bots can only access messages they can see, so make sure to send a new message after adding the bot to the group.

Finding User IDs

To find a user's Telegram ID, you have several options:

1. Using the @userinfobot:
   - Start a chat with @userinfobot on Telegram
   - Forward a message from the user whose ID you want to find to this bot
   - The bot will reply with information about the user, including their ID

2. Using your own bot:
   - Add the following function to your bot's code:

     @bot.message_handler(commands=['id'])
     def get_id(message):
         bot.reply_to(message, f"Your user ID is: {message.from_user.id}")

   - Users can then use the /id command to get their own ID

3. Using the API response:
   - In the same API response used to find the chat ID, look for the `"from":{"id":` field
   - This will show the user ID of the person who sent the message

Remember to add the user IDs of authorized quiz initiators to the `AUTHORIZED_USERS` list in your code.

Customizing Quiz Parameters

You can easily customize the number of questions and the duration of the quiz. Here's how:

1. Open the `quiz_bot.py` file in your favorite text editor.

2. To change the number of questions:
   - Locate the `select_quiz_questions()` function
   - Modify the following line:
     
     session_questions = random.sample(quiz_questions, min(5, len(quiz_questions)))

   - Change `5` to your desired number of questions

3. To change the quiz duration:
   - Locate the `start_quiz_session()` function
   - Modify the following lines:

     for i in range(5):
         threading.Timer(i * 2 * 60, send_quiz).start()
     
     threading.Timer(10 * 60, end_quiz_session).start()

   - In the first line, change `5` to match your new number of questions
   - In the first line, change `2 * 60` to adjust the time between questions (in seconds)
   - In the second line, change `10 * 60` to set the total quiz duration (in seconds)

For example, to create a quiz with 8 questions over 20 minutes:


for i in range(8):
    threading.Timer(i * 2.5 * 60, send_quiz).start()

threading.Timer(20 * 60, end_quiz_session).start()


This will send 8 questions, one every 2.5 minutes, over a total of 20 minutes.

Remember to update the quiz start message in `start_quiz_session()` to reflect your changes:


bot.send_message(QUIZ_CHAT_ID, f"SOFA.org Quiz session starting! {num_questions} quizzes will be sent over the next {duration} minutes.")


How It Works

1. The bot initializes with a predefined set of questions.
2. Authorized users can start a quiz session using the `/startquiz` command.
3. When a session starts, the bot selects a random subset of questions.
4. Questions are sent as polls to the specified chat at regular intervals.
5. Users in the chat can answer the polls.
6. The bot tracks correct answers for each user.
7. At the end of the session, the bot sends a summary of scores.

Contributing

Contributions are welcome! Feel free to expand the question pool, add new features, or improve existing functionality.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a pull request

Please make sure to update tests as appropriate.

Troubleshooting

- If the bot doesn't respond, check if you've entered the correct bot token.
- Ensure the bot has been added to the group and has the necessary permissions.
- If questions aren't sending, check if `QUIZ_CHAT_ID` is set correctly.
- For any other issues, check the console for error messages.
