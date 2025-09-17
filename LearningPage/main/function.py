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
    topic = data.get("topic")
    subject = data.get("subject")
    description = data.get("description")
    answer = data.get("answer")

    task = Task(
       topic = topic,
       subject = subject,
       description = description,
       answer = answer
    )

    try:
       task.save()
       return True
    except:
        print("Coś poszło nie tak z zadaniem")
        return False

def create_quizz(data):
    pass