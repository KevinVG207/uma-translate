import math
import util
from tqdm import tqdm
from multiprocessing import Pool
from itertools import repeat


FONT = util.prepare_font()


def add_slogan_tag(text):
    return "<slogan>" + text

def add_rbr_tag(text):
    return "<rbr>" + text


def add_scale_tag(text, max_width):
    cur_width = util.get_text_width(text, FONT)
    if cur_width <= max_width:
        return text
    
    scale_factor = math.floor(max_width / cur_width * 100)

    return f"<sc={scale_factor}>{text}"

def scale_to_box(text, max_width, max_height, line_spacing=0.9):
    # Find text scaling so it fits in a box with wrapping on spaces.
    global FONT
    line_height = 1000 * line_spacing

    scale = 100
    hyphenation = False
    while True:
        true_scale = scale / 100.
        lines = util.wrap_text_to_width(text, max_width, FONT, true_scale, hyphenation)
        height = (1 + lines.count("\n")) * line_height * true_scale

        if height <= max_height:
            break

        if not hyphenation:
            hyphenation = True
            continue

        scale -= 1
        if scale <= 0:
            print("Warning: Couldn't scale text to fit box")
            break
    
    text = lines.replace("\n", "<br>")

    if scale < 100:
        text = f"<sc={scale}>{text}"

    return text


PP_FUNCS = {
    # Slogans
    ("text_data", "144"): [(add_slogan_tag, None)],
    
    # Support cards
    ("text_data", "76"): [(add_scale_tag, (14800,))],

    # Outfits
    ("text_data", "5"): [(add_scale_tag, (14800,))],

    # Chara names
    ("text_data", "6"): [(add_scale_tag, (9500,))],
    ("text_data", "77"): [(add_scale_tag, (9500,))],
    ("text_data", "78"): [(add_scale_tag, (9500,))],
    ("text_data", "170"): [(add_scale_tag, (9500,))],

    # Skill names
    ("text_data", "47"): [(add_scale_tag, (13110,))],
    ("text_data", "48"): [(scale_to_box, (18630, 4000)), (add_rbr_tag, None)],
}


def process_mdb(args):
    entry, key = args

    # Clean up any previous processed data
    if 'processed' in entry:
        del entry['processed']

    if not entry.get('text'):
        return entry

    if key in PP_FUNCS:
        processed = entry['text']
        for func in PP_FUNCS[key]:
            pp_func, pp_args = func

            if pp_args:
                processed = pp_func(processed, *pp_args)
            else:
                processed = pp_func(processed)
            
        if processed != entry['text']:
            entry['processed'] = processed
    
    return entry


def fix_mdb():
    for mdb_json_path in tqdm(util.get_tl_mdb_jsons(), desc="Postprocessing MDBs"):
        key = util.split_mdb_path(mdb_json_path)
        data = util.load_json(mdb_json_path)

        keys, values = zip(*data.items())

        # if key in PP_FUNCS:
        #     with Pool() as p:
        #         values = p.map(process_mdb, zip(values, repeat(key)))
            
        #     data = dict(zip(keys, values))
        
        # else:
        #     for i, entry in enumerate(values):
        #         data[keys[i]] = process_mdb((entry, key))


        for entry in data.values():
            # Clean up any previous processed data
            if 'processed' in entry:
                del entry['processed']

            if not entry.get('text'):
                continue

            if key in PP_FUNCS:
                processed = entry['text']
                for func in PP_FUNCS[key]:
                    pp_func, pp_args = func

                    if pp_args:
                        processed = pp_func(processed, *pp_args)
                    else:
                        processed = pp_func(processed)
                    
                if processed != entry['text']:
                    entry['processed'] = processed
        
        util.save_json(mdb_json_path, data)


def do_postprocess():
    print("Postprocessing start")

    fix_mdb()

    print("Postprocessing done")


def main():
    do_postprocess()
    # a = "If you're in the middle of the pack during the Final Straight, and you've overtaken someone since entering the final corner, your speed will increase (bonus duration if you're not popular)"
    # # a = "someone since entering the final corner, your"
    # b = util.get_text_width(a, FONT)
    # print(b)
    # print(b * 0.8)
    # d = scale_to_box(a, 18630, 4000)
    # print(d)


if __name__ == "__main__":
    main()
