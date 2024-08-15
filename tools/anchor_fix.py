import os
import re
import sys

# Fix ctx.bumps.get("{string}").map(|bump| *bump) to Some(ctx.bumps.{string})
def fix_bumps_get_to_bumps(content: str):
    return re.subn(r'ctx\.bumps\.get\("([^"]+)"\)\.map\(\|bump\| \*bump\)', r'Some(ctx.bumps.\1)', content)

# Fix: {string + int}_array: Mutable<[{string + int}; {int}]> to {string + int}_array: [{string + int}; {int}]
def fix_mutable_array(content: str):
    return re.subn(r'([a-zA-Z0-9_]+)_array[\s\n]*?:[\s\n]*?Mutable[\s\n]*?<[\s\n]*?\[[\s\n]*?([a-zA-Z0-9]+)[\s\n]*?;[\s\n]*?(\d+)[\s\n]*?\][\s\n]*?>', r'\1_array: [\2; \3]', content)

# Fix: mut {string + int}_array: Mutable<[{string + int}; {int}]> to mut {string + int}_array: [{string + int}; {int}]
def fix_mut_mutable_array(content: str):
    return re.subn(r'mut ([a-zA-Z0-9_]+)_array: Mutable<\[([a-zA-Z0-9]+); (\d+)\]>', r'mut \1_array: [\2; \3]', content)

# Fix: $1([a-zA-Z0-9_]+).borrow().$2([a-zA-Z0-9_]+)_$3([a-zA-Z0-9]+)_$4(\d+)_array == $5([a-zA-Z0-9_]+)
# to : $1.borrow().$2_$3_$4_array == Mutable::<[$3; $4]>::new($5)
def fix_equal_borrow_data(content: str):
    return re.subn(r'([a-zA-Z0-9_]+)\.borrow\(\)\.([a-zA-Z0-9_]+)_([a-zA-Z0-9]+)_([0-9]+)_array[\s\n]*?==[\s\n]*?([a-zA-Z0-9_]+)', r'\1.borrow().\2_\3_\4_array == Mutable::<[\3; \4]>::new(\5)', content)

# Fix: $1([a-zA-Z0-9_]+).borrow().$2([a-zA-Z0-9_]+)_$3([a-zA-Z0-9]+)_class == $4([a-zA-Z0-9_]+)
# to : $1.borrow().$2_$3_class == Mutable::<$3>::new($4)
def fix_equal_borrow_class(content: str):
    return re.subn(r'([a-zA-Z0-9_]+)\.borrow\(\)\.([a-zA-Z0-9_]+)_([a-zA-Z0-9]+)_class[\s\n]*?==[\s\n]*?([a-zA-Z0-9_]+)', r'\1.borrow().\2_\3_class == Mutable::<\3>::new(\4)', content)

# Fix: assign!($1{string + int}.borrow_mut().$2{string + int}_$3{string + int}_$4{int}_array, $5{string + int}_array);
# to : assign!($1{string + int}.borrow_mut().$2{string + int}_$3{string + int}_$4{int}_array, Mutable::<[$3; $4]>::new($5{string + int}_array));
def fix_assign_borrow_mut_data(content: str):
    return re.subn(r'assign!\([\s\n]*?([a-zA-Z0-9_]+)\.borrow_mut\(\)\.([a-zA-Z0-9_]+)_([a-zA-Z0-9]+)_([0-9]+)_array[\s\n]*?,[\s\n]*?([a-zA-Z0-9_]+)_array[\s\n]*?\);', r'assign!(\1.borrow_mut().\2_\3_\4_array, Mutable::<[\3; \4]>::new(\5_array));', content)

# Fix: $1([a-zA-Z0-9_]+)_class : Mutable < $2([a-zA-Z0-9_]+) > or $1([a-zA-Z0-9_]+)_class: Mutable<$2([a-zA-Z0-9_]+)>
# To: $1_class: $2
def fix_mutable_class(content: str):
    return re.subn(r'([a-zA-Z0-9_]+)_class[\s\n]*?:[\s\n]*?Mutable[\s\n]*?<[\s\n]*?([a-zA-Z0-9]+)[\s\n]*?>', r'\1_class: \2', content)

# Fix: mut $1([a-zA-Z0-9_]+)_class: Mutable<$2([a-zA-Z0-9_]+)>
# to : mut $1_class: $2
def fix_mut_mutable_class(content: str):
    return re.subn(r'mut ([a-zA-Z0-9_]+)_class: Mutable<([a-zA-Z0-9]+)>', r'mut \1_class: \2', content)

# Fix: assign!($1([a-zA-Z0-9_]+).borrow_mut().$2([a-zA-Z0-9_]+)_$3([a-zA-Z0-9_]+)_class, $4([a-zA-Z0-9_]+));
# to : assign!($1.borrow_mut().$2_$3_class, Mutable::<$3>::new($4));
def fix_assign_borrow_mut_class(content: str):
    return re.subn(r'assign!\([\s\n]*?([a-zA-Z0-9_]+)\.borrow_mut\(\)\.([a-zA-Z0-9_]+)_([a-zA-Z0-9]+)_class[\s\n]*?,[\s\n]*?([a-zA-Z0-9_]+)[\s\n]*?\);', r'assign!(\1.borrow_mut().\2_\3_class, Mutable::<\3>::new(\4));', content)

# Fix: #[derive(Clone, Debug, Default)]
# to : #[derive(Clone, AnchorSerialize, AnchorDeserialize, Debug, Default)]
def fix_derive(content: str):
    return re.subn(r'#\[derive\(Clone, Debug, Default\)\]', r'#[derive(Clone, AnchorSerialize, AnchorDeserialize, Debug, Default)]', content)

# Fix: let mut $1([a-zA-Z0-9_]+)_mut_$2([a-zA-Z0-9]+)_$3(\d+)_array = $4([a-zA-Z0-9_]+)_array;
# to : let mut $1_mut_$2_$3_array = Mutable::<[$2, $3]>::new($4_array);
# Fix: let mut $1([a-zA-Z0-9_]+)_mut_$2([a-zA-Z0-9]+)_class = $3([a-zA-Z0-9_]+)_array;
# to : let mut $1_mut_$2_array = Mutable::<$2>::new($3_array);
def fix_let_mut_alias(content: str):
    content_temp1 = re.subn(r'let mut ([a-zA-Z0-9_]+)_mut_([a-zA-Z0-9]+)_([0-9]+)_array = ([a-zA-Z0-9_]+)_array;', r'let mut \1_mut_\2_\3_array = Mutable::<[\2; \3]>::new(\4_array);', content)
    content_temp2 = re.subn(r'let mut ([a-zA-Z0-9_]+)_mut_([a-zA-Z0-9]+)_class = ([a-zA-Z0-9_]+)_array;', r'let mut \1_mut_\2_array = Mutable::<\2>::new(\3_array);', content_temp1[0])
    return content_temp2[0], (content_temp1[1] + content_temp2[1])

# Fix: $1([a-zA-Z0-9_]+)_$2([a-zA-Z0-9]+)_class
# to : $1_class
def fix_name_mut_class(content: str):
    return re.subn(r'([a-zA-Z0-9_]+)_([a-zA-Z0-9]+)_class', r'\1_class', content)

# Fix: $1([a-zA-Z0-9_]+)_$2([a-zA-Z0-9]+)_$3(\d+)_array
# to : $1_array
def fix_name_mut_array(content: str):
    return re.subn(r'([a-zA-Z0-9_]+)_([a-zA-Z0-9]+)_(\d+)_array', r'\1_array', content)

# Function fix file
def fix_lib_rs(content: str) -> str:
    listFix = [
        fix_bumps_get_to_bumps,
        fix_mutable_array,
        fix_mutable_class,
        fix_name_mut_class,
        fix_name_mut_array,
    ]
    cnt_sum = 0
    for fix in listFix:
        content, cnt = fix(content)
        print(f"- Fixed {cnt} issues in {fix.__name__}")
        cnt_sum += cnt
    return content, cnt_sum

def fix_program_rs(content: str) -> str:
    listFix = [
        fix_mut_mutable_array,
        fix_assign_borrow_mut_data,
        fix_mut_mutable_class,
        fix_assign_borrow_mut_class,
        fix_derive,
        fix_equal_borrow_data,
        fix_equal_borrow_class,
        fix_let_mut_alias,
        fix_name_mut_class,
        fix_name_mut_array,
    ]
    cnt_sum = 0
    for fix in listFix:
        content, cnt = fix(content)
        print(f"- Fixed {cnt} issues in {fix.__name__}")
        cnt_sum += cnt
    return content, cnt_sum

# Read file and fix content
def main(prefix: str = ''):
    fix_object = {
        'lib.rs': fix_lib_rs,
        'dot/program.rs': fix_program_rs,
    }
    for filename, fix in fix_object.items():
        full_filename = os.path.join(prefix, filename)
        if os.path.exists(full_filename):
            with open(full_filename, 'r') as file:
                content = file.read()
            with open(full_filename, 'w') as file:
                content, cnt = fix(content)
                file.write(content)
                print(f'Fixed total {cnt} issues in {full_filename}')
        else:
            print(f'File {full_filename} not found')

if __name__ == '__main__':
    main(os.path.join(os.getcwd() , sys.argv[1]))