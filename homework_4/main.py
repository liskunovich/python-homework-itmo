import multiprocessing
import queue
import time
import codecs
from datetime import datetime
from typing import NoReturn

class MessageProcessor:
    @staticmethod
    def create_log_entry(message: str) -> str:
        return f"[{datetime.now().isoformat()}] {message}"

    @staticmethod
    def run_logger(log_queue: multiprocessing.Queue) -> NoReturn:
        with open("message_processing.log", "a", encoding="utf-8") as log_file:
            while True:
                try:
                    log_entry = log_queue.get(block=True)
                    log_file.write(log_entry + "\n")
                    log_file.flush()
                    print(log_entry)
                except queue.Empty:
                    continue

    @staticmethod
    def process_step_a(
        output_queue: multiprocessing.Queue,
        input_queue: multiprocessing.Queue,
        log_queue: multiprocessing.Queue
    ) -> NoReturn:
        while True:
            try:
                message = input_queue.get(block=True, timeout=1)
                
                log_queue.put(MessageProcessor.create_log_entry(
                    f"Process A: Received: '{message}'"
                ))
                
                processed_message = message.lower()
                time.sleep(5)  
                
                log_queue.put(MessageProcessor.create_log_entry(
                    f"Process A: Converted to lowercase: '{processed_message}'"
                ))
                
                output_queue.put(processed_message)
            except queue.Empty:
                continue

    @staticmethod
    def process_step_b(
        output_queue: multiprocessing.Queue,
        input_queue: multiprocessing.Queue,
        log_queue: multiprocessing.Queue
    ) -> NoReturn:
        while True:
            try:
                message = input_queue.get(block=True, timeout=1)
                
                log_queue.put(MessageProcessor.create_log_entry(
                    f"Process B: Received: '{message}'"
                ))
                
                encoded_message = codecs.encode(message, 'rot_13')
                
                log_queue.put(MessageProcessor.create_log_entry(
                    f"Process B: ROT13 encoded: '{encoded_message}'"
                ))
                
                output_queue.put(encoded_message)
            except queue.Empty:
                continue


class MessagePipeline:
    def __init__(self):
        self.to_process_a = multiprocessing.Queue()
        self.a_to_b = multiprocessing.Queue()
        self.b_to_main = multiprocessing.Queue()
        self.log_queue = multiprocessing.Queue()

        self.processes = []

    def start_workers(self) -> None:
        self.processes = [
            multiprocessing.Process(
                target=MessageProcessor.run_logger,
                args=(self.log_queue,)
            ),
            multiprocessing.Process(
                target=MessageProcessor.process_step_a,
                args=(self.a_to_b, self.to_process_a, self.log_queue)
            ),
            multiprocessing.Process(
                target=MessageProcessor.process_step_b,
                args=(self.b_to_main, self.a_to_b, self.log_queue)
            )
        ]

        for process in self.processes:
            process.start()

        self.log_queue.put(MessageProcessor.create_log_entry(
            "System: All worker processes started"
        ))

    def shutdown(self) -> None:
        for process in self.processes:
            if process.is_alive():
                process.terminate()

        self.log_queue.put(MessageProcessor.create_log_entry(
            "System: All worker processes terminated"
        ))

    def process_message(self, message: str) -> str:
        self.log_queue.put(MessageProcessor.create_log_entry(
            f"Main: Sending message for processing: '{message}'"
        ))
        
        self.to_process_a.put(message)
        
        try:
            result = self.b_to_main.get(block=True, timeout=6)
            self.log_queue.put(MessageProcessor.create_log_entry(
                f"Main: Received processed message: '{result}'"
            ))
            return result
        except queue.Empty:
            self.log_queue.put(MessageProcessor.create_log_entry(
                "Error: Timeout waiting for processed message"
            ))
            return None


def main():
    pipeline = MessagePipeline()
    
    try:
        pipeline.start_workers()
        
        while True:
            user_input = input("Enter message (or 'quit' to exit): ").strip()
            
            if user_input.lower() == 'quit':
                break
                
            if not user_input:
                continue
                
            result = pipeline.process_message(user_input)
            
            if result is not None:
                print(f"Processed result: {result}")
            else:
                print("Processing timed out")
                
    finally:
        pipeline.shutdown()


if __name__ == "__main__":
    main()
