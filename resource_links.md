Links to valuable resources
[Matt Layman Django Series](https://www.mattlayman.com/understand-django/administer-all-the-things/)
[POS tagging in Spacy](https://machinelearningknowledge.ai/tutorial-on-spacy-part-of-speech-pos-tagging/)
[The N+1 Django Query Problem](https://scoutapm.com/blog/django-and-the-n1-queries-problem)
[Git Terminology](https://opensource.com/article/19/2/git-terminology)
Fix RuntimeError: populate() isn't reentrant
    his is caused by a bug in your Django settings somewhere. Unfortunately, Django's hiding the bug behind this generic and un-useful error message. 
    To reveal the true problem, open django/apps/registry.py and around line 80, replace:

    raise RuntimeError("populate() isn't reentrant")
    with:
    self.app_configs = {}
    This will allow Django to continue loading, and reveal the actual error.

    I've encountered this error for several different causes. Once was because I had a bad import in one of my app's admin.py.

Django error: RecursionError: maximum recursion depth exceeded
    Caused by wrong config in passenger_wsgi and wsgi modules

[NLTK POS tagging](https://www.learntek.org/blog/categorizing-pos-tagging-nltk-python/)