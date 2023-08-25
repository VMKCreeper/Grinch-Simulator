# RYAN
import datetime

class Timer:
    def __init__(self, initial: int) -> None:
        self.initial = initial
    
    def countdown(self) -> bool:
        """Starts and decreases a countdown
            
        Returns:
            bool: Returns True if the countdown ends
        """
        if self.initial <= 0:
            return True
        else:
            self.initial -= 1/60

    def convert_to_datetime(self, start_index: int, end_index: int) -> str:
        """Converts timer to datetime
        
        Args:
            start_index (int): Slices the start of the string
            end_index (int): Slices the end of the string
        
        Returns:
            str: Sliced string with the seconds left in the timer 
        """
        
        return str(datetime.timedelta(seconds = self.initial))[start_index:end_index]
    
    def get_elapsed_time(self, total: int, start_index: int, end_index: int) -> str:
        """Converts timer to datetime
        
        Args:
            total (int): Total amount of time
            start_index (int): Slices the start of the string
            end_index (int): Slices the end of the string
        
        Returns:
            str: Sliced string with the total time subtracted by remaining time
        """
        
        return str(datetime.timedelta(seconds = total - self.initial))[start_index:end_index]
