from django.db import models
from jsonfield import JSONField

# Create your models here.
class Action(models.Model):
    name = models.CharField(max_length=30)
    duration = models.IntegerField(default=0)
    values = JSONField()

# Ex. firstfloor : [kitchen, living]. kitchen : [kitchen red, kitchen blue] == [kitchen 0, kitchen 1]. kitchen 0 -> Node(k0). kitchen red -> Node(k0)
# Searching
# IF the first result only has the first word (and not the second), recurse down and find all the leaves, select all the have the second word
class NodeMap(models.Model):
    name = models.CharField(max_length=30)
    virtualnodes = models.ManyToManyField('self', symmetrical=False)
    node = models.ForeignKey('node', null=True, blank=True)
    channel = models.IntegerField()

    def find_root_nodes(query):
        # query possiblities: firstfloor, firstfloor red, kitchen, kitchen red, kitchen 0, (red?)
        return None


class Node(models.Model):
    address = models.IntegerField()
    channels = models.IntegerField(default=8)
