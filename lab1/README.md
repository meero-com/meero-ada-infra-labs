# Meero x ADA - Lab 1 <!-- omit in toc -->

In this lab, you will learn how to host a static HTML file with 2 assets in a simple way, using S3.

- [Should I modify some files?](#should-i-modify-some-files)
  - [`bucket_policy.json`](#bucket_policyjson)
  - [`index.html`](#indexhtml)
- [Should I add some files?](#should-i-add-some-files)
  - [`background.jpg`](#backgroundjpg)
  - [`cv.pdf`](#cvpdf)
- [Resources names](#resources-names)

## Should I modify some files?

Yes you do! Take a look at instructions below for more informations.

### [`bucket_policy.json`](bucket_policy.json)

In this file, you must modify the line 12 by replacing `<YOUR_BUCKET_NAME_HERE>` by your bucket name:

```json
"Resource": "arn:aws:s3:::<YOUR_BUCKET_NAME_HERE>/*"
```

In example, if my bucket name is `toto`, then the line will look like this:

```json
"Resource": "arn:aws:s3:::toto/*"
```

### [`index.html`](index.html)

In this file, you will have to replace all `YOUR NAME` statement by your name.

## Should I add some files?

Yes, you do!

### `background.jpg`

You will need to select a *720p* or *1080p* **JPG** image that will be used as background. Name it `background.jpg`.

### `cv.pdf`

You will need to add your resume (CV) to this folder. It must be in **PDF** format. Name it `cv.pdf`.

## Resources names

Resources names are case sensitive, so you will have to carefully respect the following naming:

```console
$ tree
.
├── background.jpg
├── bucket_policy.json
├── cv.pdf
├── index.html
└── README.md

0 directories, 5 files
```
