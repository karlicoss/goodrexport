

Export/takeout for your personal Goodreads data

<!-- Keep this separator: Quarto otherwise moves the generated preamble below the following heading. -->

# Setting up

1.  The easiest way is `pip3 install --user git+https://github.com/karlicoss/goodrexport`.

    Alternatively, clone the repository and run `pip3 install --editable .`.

2.  [get your API keys](https://www.goodreads.com/api/keys)

# Exporting

Usage:

**Recommended**: create `secrets.py` keeping your API parameters, e.g.:

    user_id = "USER_ID"
    key = "KEY"

After that, use:

    python3 -m goodrexport.export --secrets /path/to/secrets.py

That way you type less and have control over where you keep your plaintext secrets.

**Alternatively**, you can pass parameters directly, e.g.

    python3 -m goodrexport.export --user_id <user_id> --key <key>

However, this is verbose and prone to leaking your keys/tokens/passwords in shell history.

You can also import `goodrexport.export` as a module and call `get_xml` function directly to get raw XML.

I **highly** recommend checking exported files at least once just to make sure they contain everything you expect from your export.
If they don’t, please feel free to ask or raise an issue!

# Using data

You can use this DAL (Data Access/Abstraction Layer) module to access your exported data, even offline.
I elaborate on motivation behind it [here](https://beepb00p.xyz/exports.html#dal).

- the main use case is importing it as a Python module for **programmatic access** to your data.

  You can find some inspiration in [`my.`](https://beepb00p.xyz/mypkg.html) package that I’m using as an API to all my personal data.

- to test it against your export, simply run: `python3 -m goodrexport.dal /path/to/export`

- you can also try it interactively in an IPython shell: `python3 -m goodrexport.dal /path/to/export --interactive`

# Updating README

This README is generated from a ‘literate’ Quarto [README.qmd](README.qmd) via the following command:

`tox -e quarto`

If you want to correct something, feel free to simply update `README.md` though, I can reconcile the changes next time I regenerate it.
