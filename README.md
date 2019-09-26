# HTTP Class Design Exercise

An exercise from Prof. Ousterhout's [CS 190: Software Design Studio](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter19/index.php) Winter 2019 class.

* [HTTP Design Exercise](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter19/lecture.php?topic=httpExercise)
* [Slides](https://web.stanford.edu/~ouster/cgi-bin/cs190-spring16/slides/httpExercise.pptx)

Looks like this exercise was part of a bigger exercise from [2015 Spring](https://web.stanford.edu/~ouster/cgi-bin/cs190-spring15/index.php) course.

* [Tweeter Project Introduction](https://web.stanford.edu/~ouster/cgi-bin/cs190-spring15/lecture.php?topic=tweeter), [Slides](https://web.stanford.edu/~ouster/cgi-bin/cs190-spring15/slides/tweeter.pptx)
* [CS190 Tweeter Project 1](https://web.stanford.edu/~ouster/cgi-bin/cs190-spring15/tweeter.php) See "Using HTTP for Requests" and "Results and JSON"

AFAIU, the goal is to design a general purpose HTTP class that makes it easy to write web server. It is responsible of

* implementing HTTP protocol by
* providing access to request information in a structured way
* and formatting responses in HTTP
