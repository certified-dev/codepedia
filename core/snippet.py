def upvote_question_points(self):
        self.points += 2
        self.save()

    def downvote_question_points(self):
        self.points -= 1
        self.save()

