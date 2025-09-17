from .models import Article, Task
def create_article(data):
    topic = data.get("topic")
    subject = data.get("subject")
    description = data.get("description")

    article = Article(
       topic = topic,
       subject = subject,
       description = description
    )

    try:
       article.save()
       return True
    except:
        print("Coś poszło nie tak z artkułem")
        return False
        
def create_task(data):
    pass

def create_quizz(data):
    pass