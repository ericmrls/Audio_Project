# TTS - Text To Speech

In order to use the TTS module you will have to install a library, TTS from CoquiAI. We have decided to install it by downloading it from their github, but in their [official documentation](https://github.com/coqui-ai/TTS) there are other possible methods.

```console
git clone https://github.com/coqui-ai/TTS
pip install -e .[all,dev,notebooks,tf]  # Select the relevant extras
```

You will also have to download the corresponding models.