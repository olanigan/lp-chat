import time

def logtime(func):
  """
  Decorator to log the execution time of a function.

  Args:
    func: The function to decorate.

  Returns:
    A decorated function that logs its execution time.
  """

  def wrapper(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    minutes, seconds = divmod(execution_time, 60)
    print(f"Function {func.__name__} executed in {minutes:.0f} minutes and {seconds:.3f} seconds.")
    return result

  return wrapper


# Helper function for printing docs
def get_metadata(info):
    return f"{info['source'].replace('docs/','')}, Page {info['page']}"

def pretty_print_docs(docs):
    return f"\n{'-' * 100}\n".join([f"Source {i+1}: " + get_metadata(d.metadata) + ":\n\n" + d.page_content for i, d in enumerate(docs)])