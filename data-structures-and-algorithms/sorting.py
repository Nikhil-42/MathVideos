from manim import *
import random

_SEED = 0
_LIST_LENGTH = 10
_BOX_SIZE = 1

class SelectionSortInplace(Scene):
    def __init__(self, *args, list_length = _LIST_LENGTH, **kwargs):
        super().__init__(*args, **kwargs)
        self.__list_length = list_length
    
    def setup(self):
        random.seed(_SEED)
        
        # Create list
        self.boxes = VGroup(*(
            Square(_BOX_SIZE)
                .set_fill(WHITE, opacity=0.0)
            for i in range(self.__list_length)
        )).arrange(buff=0.0)
        
        # Create random data
        self.numbers = VGroup(*(
            Integer(num + 1)
                .move_to(self.boxes[i])
            for i, num in enumerate(random.sample(range(self.__list_length), self.__list_length))
        ))

    def construct(self):        
        # Render list        
        self.play(Create(self.boxes))
        
        # Render data
        self.play(Write(self.numbers))
        
        # Create pointers
        selection_pointer = Square(1.05 * _BOX_SIZE).set_color(YELLOW).move_to(self.boxes[0])
        search_pointer = selection_pointer.copy().set_color(BLUE)
        min_pointer = search_pointer.copy().set_color(GREEN)
        
        for i in range(self.__list_length - 1):
            self.play(selection_pointer.animate.move_to(self.boxes[i]))
            min_value = float('inf')
            min_index = -1
            for j in range(i, self.__list_length):
                self.play(search_pointer.animate.move_to(self.boxes[j]))
                if self.numbers[j].number < min_value:
                    self.play(min_pointer.animate.move_to(search_pointer))
                    min_value = self.numbers[j].number
                    min_index = j
            self.play(self.numbers[i].animate.next_to(self.boxes[i], UP))
            self.play(self.numbers[min_index].animate.move_to(self.boxes[i]))
            self.play(self.numbers[i].animate.move_to(self.boxes[min_index]))
            self.numbers[i], self.numbers[min_index] = self.numbers[min_index], self.numbers[i]
            
        self.wait()

        
class SelectionSortCopy(Scene):  
    def __init__(self, *args, list_length = _LIST_LENGTH, **kwargs):
        super().__init__(*args, **kwargs)
        self.__list_length = list_length
        
    def setup(self):
        random.seed(_SEED)
        
        # Create list
        self.original_boxes = VGroup(*(
            Square(_BOX_SIZE)
                .set_fill(WHITE, opacity=0.0)
            for i in range(self.__list_length)
        )).arrange(buff=0.0).move_to(_BOX_SIZE * UP)
        
        self.sorted_boxes = self.original_boxes.copy().move_to(_BOX_SIZE * DOWN)
        
        # Create random data
        self.numbers = VGroup(*(
            Integer(num + 1)
                .move_to(self.original_boxes[i])
            for i, num in enumerate(random.sample(range(self.__list_length), self.__list_length))
        ))
    
    def construct(self):        
        # Render list
        self.play(Create(self.original_boxes))
        self.play(Create(self.sorted_boxes))
        
        # Render data
        self.play(Write(self.numbers))
        
        # Create pointers
        selection_pointer = Square(1.05 * _BOX_SIZE, color=YELLOW).move_to(self.sorted_boxes[0])
        search_pointer = selection_pointer.copy().set_color(BLUE).move_to(self.original_boxes[0])
        min_pointer = search_pointer.copy().set_color(GREEN)
        
        self.play(Create(selection_pointer))
        
        self.wait()
        self.play(Create(search_pointer))
        self.play(Create(min_pointer))
        
        used = []
        for i in range(self.__list_length):
            self.play(selection_pointer.animate.move_to(self.sorted_boxes[i]))
            min_value = float('inf')
            min_index = -1
            for j in (j for j in range(len(self.numbers)) if j not in used):
                self.play(search_pointer.animate.move_to(self.numbers[j]))
                if self.numbers[j].number < min_value:
                    self.play(min_pointer.animate.move_to(search_pointer))
                    min_value = self.numbers[j].number
                    min_index = j
            used.append(min_index)
            self.play(self.numbers[min_index].animate.move_to(self.sorted_boxes[i]))
        self.wait()


class InsertionSort(Scene):
    def __init__(self, *args, list_length = _LIST_LENGTH, **kwargs):
        super().__init__(*args, **kwargs)
        self.__list_length = list_length
    
    def construct(self):
        random.seed(_SEED)
        
        # Create list
        self.boxes = VGroup(*(
            Square(_BOX_SIZE)
                .set_fill(WHITE, opacity=0.0)
            for i in range(self.__list_length)
        )).arrange(buff=0)
        
        # Create random data
        self.numbers = VGroup(*(
            Integer(num + 1)
                .move_to(self.boxes[i])
            for i, num in enumerate(random.sample(range(self.__list_length), self.__list_length))
        ))
        
        # Render list
        self.play(Create(self.boxes))
        
        # Render data
        self.play(Write(self.numbers))
        
        # Create regions
        insertion_pointer = Rectangle(color=YELLOW, height=1.05*_BOX_SIZE, width=2.05*_BOX_SIZE).move_to(self.boxes[0].get_center() + 0.5 * _BOX_SIZE * RIGHT)
        sorted_region = Rectangle(GREEN, height=1.05*_BOX_SIZE, width=0.025*_BOX_SIZE).align_to(insertion_pointer, LEFT)
        unsorted_region = Rectangle(RED, height=1.05*_BOX_SIZE, width=(self.__list_length + 0.025) * _BOX_SIZE).align_to(insertion_pointer, LEFT).shift(RIGHT * 0.05 * _BOX_SIZE)
        
        self.play(
            sorted_region.animate.stretch_about_point((sorted_region.width + _BOX_SIZE) / sorted_region.width, 0, point=LEFT * _BOX_SIZE * (self.__list_length/2 + 0.025)),
            unsorted_region.animate.stretch_about_point((unsorted_region.width - _BOX_SIZE) / unsorted_region.width, 0, point=RIGHT * _BOX_SIZE * (self.__list_length/2 + 0.025))
        )
        self.play(Create(insertion_pointer))
           
        for i in range(1, self.__list_length):            
            # Perform swaps
            for j in range(i, 0, -1):
                self.play(insertion_pointer.animate.move_to(self.boxes[j-1].get_center() + 0.5 * _BOX_SIZE * RIGHT))
                if self.numbers[j].number < self.numbers[j - 1].number:
                    self.play(self.numbers[j-1].animate.next_to(self.boxes[j-1], UP))
                    self.play(self.numbers[j].animate.move_to(self.boxes[j-1]))
                    self.play(self.numbers[j-1].animate.move_to(self.boxes[j]))
                    self.numbers[j], self.numbers[j-1] = self.numbers[j-1], self.numbers[j]
                else:
                    break
            self.play(insertion_pointer.animate.move_to(self.boxes[i-1].get_center() + 0.5 * _BOX_SIZE * RIGHT))

            # Update sorted an unsorted regions
            self.play(
                sorted_region.animate.stretch_about_point((sorted_region.width + _BOX_SIZE) / sorted_region.width, 0, point=LEFT * _BOX_SIZE * (self.__list_length/2 + 0.025)),
                unsorted_region.animate.stretch_about_point((unsorted_region.width - _BOX_SIZE) / unsorted_region.width, 0, point=RIGHT * _BOX_SIZE * (self.__list_length/2 + 0.025))
            )
        self.wait()
        
class BubbleSort(Scene):
    def __init__(self, *args, list_length=_LIST_LENGTH, **kwargs):
        super().__init__(*args, **kwargs)
        self.__list_length = list_length
    
    def construct(self):
        random.seed(_SEED)
        
        # Create list
        self.boxes = VGroup(*(
            Square(_BOX_SIZE)
                .set_fill(WHITE, opacity=0.0)
            for i in range(self.__list_length)
        )).arrange(buff=0)
        
        # Create random data
        self.numbers = VGroup(*(
            Integer(num + 1)
                .move_to(self.boxes[i])
            for i, num in enumerate(random.sample(range(self.__list_length), self.__list_length))
        ))
        
        # Render list
        self.play(Create(self.boxes))
        
        # Render data
        self.play(Write(self.numbers))
        
        swap_pointer = Rectangle(color=YELLOW, height=1.05*_BOX_SIZE, width=2.05*_BOX_SIZE).move_to(self.boxes[0].get_center() + 0.5 * _BOX_SIZE * RIGHT)
        
        self.play(Create(swap_pointer))  
        
        for i in range(1, self.__list_length):
            sort_complete = True
            # Perform swaps
            for j in range(1, self.__list_length):
                self.play(swap_pointer.animate.move_to(self.boxes[j-1].get_center() + 0.5 * _BOX_SIZE * RIGHT))
                if self.numbers[j].number < self.numbers[j - 1].number:
                    self.play(self.numbers[j-1].animate.next_to(self.boxes[j-1], UP))
                    self.play(self.numbers[j].animate.move_to(self.boxes[j-1]))
                    self.play(self.numbers[j-1].animate.move_to(self.boxes[j]))
                    self.numbers[j], self.numbers[j-1] = self.numbers[j-1], self.numbers[j]
                    sort_complete = False
            if sort_complete:
                break
            
class MergeSort(MovingCameraScene):
    def __init__(self, *args, list_length=_LIST_LENGTH, **kwargs):
        super().__init__(*args, **kwargs)
        self.__list_length = list_length
   
    def construct(self):
        random.seed(_SEED)
        
        # Create list
        self.boxes = VGroup(*(
            Square(_BOX_SIZE)
                .set_fill(WHITE, opacity=0.0)
            for i in range(self.__list_length)
        )).arrange(buff=0)
        
        # Create random data
        self.numbers = VGroup(*(
            Integer(num + 1)
                .move_to(self.boxes[i])
            for i, num in enumerate(random.sample(range(self.__list_length), self.__list_length))
        ))
        
        # Render list
        self.play(Create(self.boxes))
        
        # Render data
        self.play(Write(self.numbers))
       
        self.wait()
        
        def merge(lnumbers, rnumbers):
            merged_boxes = VGroup(*(
                Square(_BOX_SIZE)
                .set_fill(WHITE, opacity=0.0)
                for i in range(len(lnumbers) + len(rnumbers))
            )).arrange(buff=0).move_to(lnumbers + rnumbers).shift(1.5 * _BOX_SIZE * UP)
            self.play(Create(merged_boxes))
            
            merged = VGroup()
            lptr = 0
            rptr = 0
            for i in range(len(lnumbers) + len(rnumbers)):
                if rptr >= len(rnumbers) or (lptr < len(lnumbers) and lnumbers[lptr].number < rnumbers[rptr].number):
                    merged.add(lnumbers[lptr])
                    self.play(lnumbers[lptr].animate.move_to(merged_boxes[i]))
                    lptr += 1
                else:
                    merged.add(rnumbers[rptr])
                    self.play(rnumbers[rptr].animate.move_to(merged_boxes[i]))
                    rptr += 1

            self.play(Uncreate(merged_boxes))
            return merged
        
        def merge_sort(numbers: VGroup):
            if len(numbers) == 1:
                return numbers
            
            self.play(self.camera.frame.animate.move_to(numbers))
            self.play(numbers.animate.shift(1.5 * _BOX_SIZE * DOWN))

            lnumbers = numbers[:len(numbers)//2]
            rnumbers = numbers[len(numbers)//2:]
            
            self.play(
                lnumbers.animate.shift(0.5 * _BOX_SIZE * LEFT),
                rnumbers.animate.shift(0.5 * _BOX_SIZE * RIGHT)
            )
            
            lnumbers = merge_sort(numbers[:len(numbers)//2])
            rnumbers = merge_sort(numbers[len(numbers)//2:])

            self.play(self.camera.frame.animate.move_to(numbers))
            merged = merge(lnumbers, rnumbers)
            self.play(self.camera.frame.animate.move_to(merged))
            
            return merged

        self.sorted_numbers = merge_sort(self.numbers)

       
if __name__ == '__main__':
    MergeSort().construct() 
        