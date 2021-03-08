from django.db import models
from quizes.models import Quiz


class Question(models.Model):

    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}"

    def get_answers(self):
        """ Returns all answers to this question """
        return self.answer_set.all()


class Answer(models.Model):
    """ An answer to a question. """
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question: {self.question.text}. Answer: {self.text}. Correct: {self.correct}"

