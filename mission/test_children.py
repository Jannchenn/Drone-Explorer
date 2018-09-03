class Resource:
    class_counter = 0
    def __init__(self):
        self.id= Resource.class_counter
        Resource.class_counter += 1

class Other(Resource):
    def __init__(self):
        Resource.__init__(self)

print Resource().id
print Resource().id
print Resource().id
print Resource().id
print Other().id