import subprocess

# The filepath to the wav files of the speakers
wav_filepath = "/home/user/uni/8th_semester/nlp/lab_1/usc/wav"

# The filepath to the transcriptions
transcription_filepath = "/home/user/uni/8th_semester/nlp/lab_1/usc/transcriptions.txt"

# The filepath to the lexicon
lexicon_filepath = "/home/user/uni/8th_semester/nlp/lab_1/usc/lexicon.txt"



# The filepath to the training data we were given
source_train_filepath = "/home/user/uni/8th_semester/nlp/lab_1/usc/filesets/training.txt"

# The filepath to the validation data we were given
source_val_filepath = "/home/user/uni/8th_semester/nlp/lab_1/usc/filesets/validation.txt"

# The filepath to the testing data we were given
source_test_filepath = "/home/user/uni/8th_semester/nlp/lab_1/usc/filesets/testing.txt"



# The filepath to the files we want to generate regarding training
destination_train_filepath = "/home/user/uni/8th_semester/nlp/lab_1/kaldi/egs/usc/data/train/"

# The filepath to the files we want to generate regarding validation
destination_val_filepath = "/home/user/uni/8th_semester/nlp/lab_1/kaldi/egs/usc/data/dev/"

# The filepath to the files we want to generate regarding testing
destination_test_filepath = "/home/user/uni/8th_semester/nlp/lab_1/kaldi/egs/usc/data/test/"





# Get a sentence and replace the words with their phonemes
def convert_to_lexicon(utterance):
    special_character_list = [',', '.', '!', '?', '"', '-']
    
    sanitized_utterance = str(utterance).lower()
    for char in special_character_list:
        sanitized_utterance = sanitized_utterance.replace(char, '')

    lex = "sil"

    for word in sanitized_utterance.split(" "):
        with open(lexicon_filepath, "r") as lexicon_file:
            for line in lexicon_file:
                #print(word.lower(), line.split(" ")[0].lower())
                if word.lower() == line.split(" ")[0].strip().lower():
                    lex += " " + ' '.join(line.split(" ")[1:]).strip("\n")


    return lex + " sil"


def generate_files(start_filepath, final_filepath):

    
    write_text_uttids = ""
    write_text_utt2spk = ""
    write_text_wav = ""
    write_text_text = ""
    current_id = 0
    with open(start_filepath, "r") as file:
        for current_line in file:
            # remove the newline character
            current_line = current_line.strip("\n")
            
            # the ids are from 0 to lines-1
            write_text_uttids += f"{current_id}\n"

            # 
            write_text_utt2spk += f"{current_id} {current_line.split('_')[0]}\n"
            write_text_wav += f"{current_id} {wav_filepath}/{current_line}.wav\n"
            
            utterance_instance = current_line.split('_')[1]
            utterance_transcription = ""
            with open(transcription_filepath, "r") as transcription_file:
                for line in transcription_file:
                    if (line.split(" ")[0][:3] == utterance_instance):
                        utterance_transcription = ' '.join(line.split(" ")[1:]).strip("\n")
                        break
            
            write_text_text += f"{current_id} {convert_to_lexicon(utterance_transcription)}\n"


            current_id += 1
    
    with open(f"{final_filepath}/uttids", "w") as file:
        file.write(write_text_uttids)

    with open(f"{final_filepath}/utt2spk","w") as file:
        file.write(write_text_utt2spk)
    
    with open(f"{final_filepath}/wav.scp", "w") as file:
        file.write(write_text_wav)

    with open(f"{final_filepath}/text", "w") as file:
        file.write(write_text_text)

    

generate_files(source_train_filepath, destination_train_filepath)
generate_files(source_val_filepath, destination_val_filepath)
generate_files(source_test_filepath, destination_test_filepath)
