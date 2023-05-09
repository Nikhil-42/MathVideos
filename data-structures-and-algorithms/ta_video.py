from __future__ import annotations
from typing import Optional

from manim import *
from manim import Scene
from manim import Integer, Graph

# from manim_voiceover import VoiceoverScene
# from manim_voiceover.services.gtts import GTTSService as VoiceoverService

import random

class Node(VMobject):
    __num: int
    __left: Optional[Node] = None
    __right: Optional[Node] = None
    __height: int = 1

    __left_edge: Optional[Line] = None
    __right_edge: Optional[Line] = None
    
    def __init__(self, num: int, **kwargs):
        super().__init__(**kwargs)
        self.__num = num
        self.circle = Circle(color=WHITE).scale(1/2).scale(2/3)
        self.text = Integer(num).scale(2/3)
        self.add(self.text)
        self.add(self.circle)
        
        def update_edges(self, dt):
            if self.__left is not None and self.__left_edge is not None:
                self.__left_edge.become(Line(self.circle.get_center(), self.__left.circle.get_center(), buff=0.5*self.circle.width))
            if self.__right is not None and self.__right_edge is not None:
                self.__right_edge.become(Line(self.circle.get_center(), self.__right.circle.get_center(), buff=0.5*self.circle.width))
        self.add_updater(update_edges)
        
        self.__left_height = 0
        self.__right_height = 0
    
    def insert(self, node: Node, scene: None|Scene = None, **kwargs) -> Node:
        if scene is not None:
            scene.play(node.animate.next_to(self.circle, UP, buff=0.5), **kwargs)
        else:
            node.next_to(self.circle, UP, buff=0.5)
            
        if node.__num < self.__num:
            # insert left
            if self.__left is None:
                self.__set_left(node, scene, **kwargs)
            else:
                if scene is not None:
                    scene.play(Indicate(self.__left), **kwargs)
                self.__set_left(self.__left.insert(node, scene, **kwargs), scene, **kwargs)
        elif node.__num > self.__num:
            # insert right
            if self.__right is None:
                self.__set_right(node, scene, **kwargs)
            else:
                if scene is not None:
                    scene.play(Indicate(self.__right), **kwargs)
                self.__set_right(self.__right.insert(node, scene, **kwargs), scene, **kwargs)
        else:
            if scene is not None:
                scene.play(node.animate.set_color(RED), **kwargs)
                scene.play(Uncreate(node), **kwargs)
            
        return self
    
    def delete(self, scene: Scene|None = None, **kwargs):
        if self.__left is not None:
            self.__left.delete(scene, **kwargs)
        if self.__right is not None:
            self.__right.delete(scene, **kwargs)
        if self.__left_edge is not None:
            if scene is not None:
                scene.play(Uncreate(self.__left_edge), **kwargs)
            self.remove(self.__left_edge)
        if self.__right_edge is not None:
            if scene is not None:
                scene.play(Uncreate(self.__right_edge), **kwargs)
            self.remove(self.__right_edge)
        if scene is not None:
            scene.play(Uncreate(self), **kwargs)
            
    def balance(self, scene: Scene, **kwargs) -> Node:        
        def height(node: Node):
            return node.__height if node is not None else 0
        
        if height(self.__left) - height(self.__right) > 1:
            scene.play(Indicate(self.__left.__height_display, 2, color=RED), **kwargs)
            # left heavy
            if height(self.__left.__right) > height(self.__left.__left):
                scene.play(Indicate(self.__left.__right.__height_display, 2, color=RED), **kwargs)
                # left right case
                self.__set_left(self.__left.rotate_left(scene, **kwargs), scene, **kwargs)
            return self.rotate_right(scene, **kwargs)
        elif height(self.__right) - height(self.__left) > 1:
            scene.play(Indicate(self.__right.__height_display, 2, color=RED), **kwargs)
            # right heavy
            if height(self.__right.__left) > height(self.__right.__right):
                scene.play(Indicate(self.__right.__left.__height_display, 2, color=RED), **kwargs)
                # right left case
                self.__set_right(self.__right.rotate_right(scene, **kwargs), scene, **kwargs)
            return self.rotate_left(scene, **kwargs)
        else:
            anims = []
            if self.__left is not None:
                anims.append(Indicate(self.__left.__height_display, 2, color=GREEN))
            if self.__right is not None:
                anims.append(Indicate(self.__right.__height_display, 2, color=GREEN))
            scene.play(*anims, **kwargs)
            self.__update_height()
            return self 

    def rotate_left(self, scene: Scene, **kwargs):
        assert self.__right is not None
        
        new_root = self.__right

        self.__set_right(None, scene, **kwargs)
        
        left_height = new_root.__left.__height if new_root.__left is not None else 1
        scene.play(
            new_root.animate.move_to(self.circle.get_center() + (new_root.get_center() - new_root.circle.get_center() )),
            self.animate.shift(LEFT * self.circle.width * 2**(left_height)),
        **kwargs)
        
        self.__set_right(new_root.__left, scene, **kwargs)
        new_root.__set_left(self, scene, **kwargs)
        
        self.__update_height()
        new_root.__update_height()
        
        return new_root 
        
    def rotate_right(self, scene: Scene, **kwargs):
        assert self.__left is not None
        
        new_root = self.__left

        self.__set_left(None, scene, **kwargs)
        
        right_height = new_root.__right.__height if new_root.__right is not None else 1
        scene.play(
            new_root.animate.move_to(self.circle.get_center() + (new_root.get_center() - new_root.circle.get_center() )),
            self.animate.shift(RIGHT * self.circle.width * 2**(right_height)),
        **kwargs)
        
        self.__set_left(new_root.__right, scene, **kwargs)
        new_root.__set_right(self, scene, **kwargs)
        
        self.__update_height()
        new_root.__update_height()
        
        return new_root 
 
    def __set_left(self, node: Node, scene: Scene, **kwargs):
        # Remove the node if it exists and is not the same as the new node
        if self.__left is not None and node is not self.__left:
            self.remove(self.__left)
            
        # Remove the edge if it exists
        if self.__left_edge is not None and (node is None or node.__height != self.__left_height):
            if scene is not None:
                scene.play(Uncreate(self.__left_edge), **kwargs)
            self.remove(self.__left_edge)
            self.__left_edge = None
        
        self.__left = node
        
        # Move the node to the correct position
        if self.__left is not None:
            if scene is not None:
                scene.play(self.__left.animate.move_to(
                    self.circle.get_center() +
                    LEFT * self.circle.width * 2**(self.__left.__height-1) +
                    DOWN + 
                    (self.__left.get_center() - self.__left.circle.get_center()),
                ), **kwargs)
            else:
                self.__left.move_to(
                    self.circle.get_center() +
                    LEFT * self.circle.width * 2**(self.__left.__height-1) +
                    DOWN + 
                    (self.__left.get_center() - self.__left.circle.get_center()),
                )
                
            # Create the edge if it doesn't exist
            if self.__left_edge is None:
                self.__left_height = self.__left.__height
                self.__left_edge = Line(self.circle.get_center(), self.__left.circle.get_center(), buff=0.5*self.circle.width)
                if scene is not None:
                    scene.play(Create(self.__left_edge), **kwargs)
            self.add(self.__left, self.__left_edge)
        self.__update_height()
        
    def __set_right(self, node: Node, scene: Scene, **kwargs):
        # Remove the node if it exists and is not the same as the new node
        if self.__right is not None and node is not self.__right:
            self.remove(self.__right)
        
        # Remove the edge if it exists
        if self.__right_edge is not None and (node is None or node.__height != self.__right_height):
            self.remove(self.__right_edge)
            if scene is not None:
                scene.play(Uncreate(self.__right_edge), **kwargs)
            self.__right_edge = None
        
        self.__right = node
        
        # Move the node to the correct position
        if self.__right is not None:
            if scene is not None:
                scene.play(self.__right.animate.move_to(
                    self.circle.get_center() +
                    RIGHT * self.circle.width * 2**(self.__right.__height-1) +
                    DOWN + 
                    (self.__right.get_center() - self.__right.circle.get_center()),
                ), **kwargs)
            else:
                self.__right.move_to(
                    self.circle.get_center() +
                    RIGHT * self.circle.width * 2**(self.__right.__height-1) +
                    DOWN + 
                    (self.__right.get_center() - self.__right.circle.get_center()),
                )
            
            # Create the edge if it doesn't exist
            if self.__right_edge is None:
                self.__right_height = self.__right.__height
                self.__right_edge = Line(self.circle.get_center(), self.__right.circle.get_center(), buff=0.5*self.circle.width)
                if scene is not None:
                    scene.play(Create(self.__right_edge), **kwargs)
            self.add(self.__right, self.__right_edge)
        self.__update_height()
        
    def __update_height(self):
        self.__height = max(
            self.__left.__height if self.__left is not None else 0,
            self.__right.__height if self.__right is not None else 0,
        ) + 1
    
    def track_height(self):
        self.__height_display = Integer(self.__height).scale(0.5).move_to(self.circle.get_center() + UP * self.circle.width * 0.75)
        self.add(self.__height_display)
        
        def update_height_display(self):
            self.__height_display.set_value(self.__height)
            self.__height_display.move_to(self.circle.get_center() + UP * self.circle.width * 0.75)

        self.add_updater(update_height_display)
        
        return self
        
class AVLDemonstration(Scene):
    def construct(self):            
        root = Node(0)
        # We've already seen how a binary tree can be used to maintain a sorted list of elements.
        self.play(Create(root))
        
        # In the best-case, search, insertion, and removal of elements can happen in O(log n).
        root.insert(Node(-1), self)
        root.insert(Node(1), self)
        
        # But in the worst case, the time complexity is still O(n).
        for i in range(2,5):
            new_node = Node(i).next_to(root, UP, buff=1)
            root.insert(new_node, self)
    
        # "We can do better..."
        self.play(*(Uncreate(mob) for mob in self.mobjects))
        
        # "...by ensuring that our tree remains balanced."
        root = Node(2)
        self.play(Create(root))
        for i in (0,1,4,3):
            new_node = Node(i).next_to(root, UP, buff=1)
            root.insert(new_node, self)

        # "Notice that the data being inserted doesn't impact the balance of the tree."
        
        # "For any set of data there are actually many different valid binary trees."
        left = Node(1).shift(LEFT*5)
        right = Node(3).shift(RIGHT*5)
        self.play(Create(left), Create(right))
        
        for l, r in zip((3,0,4,2), (1,2,0,4)):
            new_node = Node(l).next_to(left, UP, buff=1)
            left.insert(new_node, self, run_time=0.05)
            new_node = Node(r).next_to(right, UP, buff=1)
            right.insert(new_node, self, run_time=0.05)
            
        # "So there should be a way to turn any tree into one that is balanced."
        
        # "Right now the root of the tree is always the first element inserted."
        # "But if one subtree is getting longer than the other, it would be better to reroot the tree at the middle of that chain
        # (so that half the nodes fall to the left and half to the right)."
        
        self.play(*(Uncreate(mob) for mob in self.mobjects))
        
        root = Node(-1)
        self.play(Create(root))
        
        for i in (0,1):
            new_node = Node(i).next_to(root, UP, buff=1)
            root.insert(new_node, self)
        
        root = root.rotate_left(self)

        self.play(*(Uncreate(mob) for mob in self.mobjects))
        
        root = Node(1)
        self.play(Create(root))
        
        for i in (0,-1):
            new_node = Node(i).next_to(root, UP, buff=1)
            root.insert(new_node, self)
        
        root = root.rotate_right(self)

        self.play(*(Uncreate(mob) for mob in self.mobjects))

        # "This is called a rotation."
        
        # If we notice the tree is unbalanced but the chain is bent, we can straighten it out with a counter-rotation.
        root = Node(-1)
        self.play(Create(root))
        
        for i in (1,0):
            new_node = Node(i).next_to(root, UP, buff=1)
            root.insert(new_node, self)
        
        root._Node__set_right(root._Node__right.rotate_right(self), self)
        root = root.rotate_left(self)

        self.play(*(Uncreate(mob) for mob in self.mobjects))
        
        # This idea of rotating chains of nodes into bushier trees is the basis of the AVL tree.
        # The last thing we need to do is decide when to rotate. The simplest way to do this is by keeping track of the height of each node.
        
        # "Now with all the intuition out of the way, let's see how this works in practice."
        root = Node(0).track_height()
        self.play(Create(root))
        
        for i in range(1, 7):
            new_node = Node(i).next_to(root, UP, buff=1).track_height()
            root.insert(new_node, self, run_time=0.5)
            root = root.balance(new_node, self, run_time=0.5)
        

if __name__ == '__main__':
    config.preview = True
    config.renderer = 'cairo'
    config.quality = 'low_quality'
    AVLDemonstration().render()