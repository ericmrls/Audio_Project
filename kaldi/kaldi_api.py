import uvicorn
from fastapi import FastAPI, File, UploadFile
import os
import re
from fastapi.responses import FileResponse

app = FastAPI()


@app.post("/stt")
async def stt(my_file: UploadFile = File(...)):
    result_path = '/kaldi/egs/wsj/s5/exp/chain_cleaned/tdnn_1d_sp/decode_test_dev93_tgsmall/scoring_kaldi/wer_details/per_utt'
    
    with open('tmp_output.wav','wb') as f:
        f.write(my_file.file.read())

    os.system('sox tmp_output.wav -r 16000 -c 1 kaldi/egs/wsj/s5/data/audio/file1.wav')
    
    os.chdir('kaldi/egs/wsj/s5/')

    os.system('. ./commands_run.sh')

    
    with open(result_path, 'r') as f:
        text = re.sub(' +', ' ', f.readlines()[1])[10:].lower()
        
    return text


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)