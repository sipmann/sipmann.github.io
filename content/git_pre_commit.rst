Using git hooks to easy your life
###########################################

:date: 2019-07-30 20:00
:tags: git, shell, pre-commit, hooks
:category: tools
:slug: using_git_hooks_easy_your_life
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:lang: en

Hey folks, it's been a time since my last post. In the meantime, I moved to another state, changed job, and started learning new kinds of stuff. Today I would like to share one thing that I usually do with my small git projects. Git has many cool features, git hooks were one of them. I'll talk about the pre-commit hook today.

Let's say that, for some reason, you don't have a CI tool/server running after every commit and you want to enforce that every developer runs the tests before every commit? Git pre-commit to the rescue. You can code the hooks with shell, ruby, python, and I could be wrong, but even PHP would work. pre-commit is a client-side hook (we have server side too) and he's located inside the `.git/hooks` folder. Let's jump to the code... Create a file called 'pre-commit' inside that folder with the following code.

.. code-block:: shell

    #!/bin/bash
    npm test # assuming you're using it inside a nodeJS project

Don't forget to make the script executable!! Now break your test and try to commit. That's easy but can save you from breaking the tests at the main CI/Travis/Codeship/etc and being notified by email :). Why not even validate the lint of your project or check if the coverage doesn't fall? Does your team/company have a patter for commit messages? No problem, there is a hook called `commit-msg` that you can use to validate your message.
