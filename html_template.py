css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #5D6D7E
}
.chat-message.bot {
    background-color: #34495E
}
.chat-message .avatar {
  width: 20%;
}
#.chat-message .avatar .h2 {
#   max-width: 78px;
#   max-height: 78px;
#   border-radius: 50%;
#   object-fit: cover;
#}
.chat-message .message {
  font-size: 20px;
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <h2> A: </h2>
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <h2> Q: </h2>
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''