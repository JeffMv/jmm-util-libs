[TOC]



# JMM lib



Library of helper functions, shortcuts and pieces of code that I reuse a lot.

Meant for my personal use and for reuse in my personal projects.



## Deploy



### On Github

See Git – [Basics of tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging) (Tags for versioning with Git & tags on Github)

Notes on "*(semantic) versioning*" : https://semver.org



#### Installing from Github

**Installing the latest version**

Stable releases are published in the `releases` branch. So to install the latest version, type:

```bash
# will install the latest version of branch `releases`
pip install git+https://github.com/JeffMv/test-python-package-creation.git@releases
```



**Installing a specific version**

```bash
# To install a specific version, for instance version with tag v0.1.2.8.4 just type
pip install git+https://github.com/JeffMv/jmm-util-libs.git@v0.1.2.8.4
```





In order to install a specific version from a git tag:

```bash
pip install -e "git://github.com/{ username }/{ reponame }.git@{ tag name }#egg={ desired egg name }"

# (source: https://coderwall.com/p/-wbo5q/pip-install-a-specific-github-repo-tag-or-branch)
```





See this answer for [Installing a specific commit with Pip](https://stackoverflow.com/a/13754517/4418092)

