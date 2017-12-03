## Data Science in a Docker container

I have spent almost a decade in finance. I have been exposed to some of the worst and best software used in industry out there. 
You know who you are...

In the old days we used to run experiments and wrote reports or created presentations. However, the way I communicate my
results and cooperate with researchers has changed. My audience isn't very homogeneous. Management may want to see a bunch of graphs whereas a fellow researcher is interested in replicating my experiments and interact with data. 

In this little note I describe my current workflow reflecting the aforementioned challenging demands 
and invite you to trash or copy it. For that purpose I have compiled a little script illustrating how I interact with 
Git, Docker, Jupyter and the Notebook Viewer.

To get a first glimpse of what I am doing try to open my Notebook via

https://nbviewer.jupyter.org/github/tschm/babynames/blob/master/books/Baby.ipynb

The nbviewer is a tool to share results with clients or management. 
People can browse through results but have very limited possibilities to interfere with the underlying program. 
They see a html page and can cause no damage. 
They don't need to have any further tools installed. No Git, No Docker... any standard browser will do.

To share my results with fellow scientists I prefer to send them a link to my Github repository. 
They can clone it and fire off exactly the same environment I have been using. 

```
git clone https://github.com/tschm/babynames.git
```
You can then run or inspect
```
start.sh
```
A Jupyter server will now run on your localhost at port 2016. 

