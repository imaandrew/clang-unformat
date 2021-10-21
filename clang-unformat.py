#!/usr/bin/env python3

import argparse
import random
import subprocess
from tqdm import tqdm

options = {
    'AccessModifierOffset': ['RANDINT', 0, 20],
    'AlignAfterOpenBracket': ['Align', 'DontAlign', 'AlwaysBreak'],
    'AlignArrayOfStructures': ['Left', 'Right'],
    'AlignConsecutiveAssignments': ['None', 'Consecutive', 'AcrossEmptyLines', 'AcrossComments', 'AcrossEmptyLinesAndComments'],
    'AlignConsecutiveBitFields': ['None', 'Consecutive', 'AcrossEmptyLines', 'AcrossComments', 'AcrossEmptyLinesAndComments'],
    'AlignConsecutiveDeclarations': ['None', 'Consecutive', 'AcrossEmptyLines', 'AcrossComments', 'AcrossEmptyLinesAndComments'],
    'AlignConsecutiveMacros': ['None', 'Consecutive', 'AcrossEmptyLines', 'AcrossComments', 'AcrossEmptyLinesAndComments'],
    'AlignEscapedNewlines': ['DontAlign', 'Left', 'Right'],
    'AlignOperands': ['DontAlign', 'Align', 'AlignAfterOperator'],
    'AlignTrailingComments': ['BOOL'],
    'AllowAllArgumentsOnNextLine': ['BOOL'],
    'AllowAllParametersOfDeclarationOnNextLine': ['BOOL'],
    'AllowShortBlocksOnASingleLine': ['Never', 'Empty', 'Always'],
    'AllowShortCaseLabelsOnASingleLine': ['BOOL'],
    'AllowShortEnumsOnASingleLine': ['BOOL'],
    'AllowShortFunctionsOnASingleLine': ['None', 'InlineOnly', 'Empty', 'Inline', 'All'],
    'AllowShortIfStatementsOnASingleLine': ['Never', 'WithoutElse', 'OnlyFirstIf', 'AllIfsAndElse'],
    'AllowShortLambdasOnASingleLine': ['None', 'Empty', 'Inline', 'All'],
    'AllowShortLoopsOnASingleLine': ['BOOL'],
    'AlwaysBreakAfterDefinitionReturnType': ['None', 'All', 'TopLevel'],
    'AlwaysBreakAfterReturnType': ['None', 'All', 'TopLevel', 'AllDefinitions', 'TopLevelDefinitions'],
    'AlwaysBreakBeforeMultilineStrings': ['BOOL'],
    'AlwaysBreakTemplateDeclarations': ['No', 'MultiLine', 'Yes'],
    'BinPackArguments': ['BOOL'],
    'BinPackParameters': ['BOOL'],
    'BitFieldColonSpacing': ['Both', 'None', 'Before', 'After'],
    'BraceWrapping': {
        'AfterCaseLabel': ['BOOL'],
        'AfterClass': ['BOOL'],
        'AfterControlStatement': ['Never', 'MultiLine', 'Always'],
        'AfterEnum': ['BOOL'],
        'AfterFunction': ['BOOL'],
        'AfterNamespace': ['BOOL'],
        'AfterObjCDeclaration': ['BOOL'],
        'AfterStruct': ['BOOL'],
        'AfterUnion': ['BOOL'],
        'AfterExternBlock': ['BOOL'],
        'BeforeCatch': ['BOOL'],
        'BeforeElse': ['BOOL'],
        'BeforeLambdaBody': ['BOOL'],
        'BeforeWhile': ['BOOL'],
        'IndentBraces': ['BOOL'],
        'SplitEmptyFunction': ['BOOL'],
        'SplitEmptyRecord': ['BOOL'],
        'SplitEmptyNamespace': ['BOOL']
    },
    'BreakAfterJavaFieldAnnotations': ['BOOL'],
    'BreakBeforeBinaryOperators': ['None', 'NonAssignment', 'All'],
    'BreakBeforeBraces': ['Custom'],
    'BreakBeforeConceptDeclarations': ['BOOL'],
    'BreakBeforeTernaryOperators': ['BOOL'],
    'BreakConstructorInitializers': ['BeforeColon', 'BeforeComma', 'AfterColon'],
    'BreakInheritanceList': ['BeforeColon', 'BeforeComma', 'AfterColon', 'AfterComma'],
    'BreakStringLiterals': ['BOOL'],
    'ColumnLimit': ['RANDINT', 5, 300],
    'CompactNamespaces': ['BOOL'],
    'ConstructorInitializerIndentWidth': ['RANDINT', 1, 20],
    'ContinuationIndentWidth': ['RANDINT', 1, 20],
    'Cpp11BracedListStyle': ['BOOL'],
    'EmptyLineAfterAccessModifier': ['Never', 'Leave', 'Always'],
    'EmptyLineBeforeAccessModifier': ['Never', 'Leave', 'LogicalBlock', 'Always'],
    'FixNamespaceComments': ['BOOL'],
    'IndentAccessModifiers': ['BOOL'],
    'IndentCaseBlocks': ['BOOL'],
    'IndentCaseLabels': ['BOOL'],
    'IndentExternBlock': ['AfterExternBlock', 'NoIndent', 'Indent'],
    'IndentGotoLabels': ['BOOL'],
    'IndentPPDirectives': ['None', 'AfterHash', 'BeforeHash'],
    'IndentRequires': ['BOOL'],
    'IndentWidth': ['RANDINT', 1, 20],
    'IndentWrappedFunctionNames': ['BOOL'],
    'JavaScriptQuotes': ['Leave', 'Single', 'Double'],
    'JavaScriptWrapImports': ['BOOL'],
    'KeepEmptyLinesAtTheStartOfBlocks': ['BOOL'],
    'LambdaBodyIndentation': ['Signature', 'OuterScope'],
    'MaxEmptyLinesToKeep': ['RANDINT', 0, 10],
    'NamespaceIndentation': ['None', 'Inner', 'All'],
    'ObjCBinPackProtocolList': ['Auto', 'Always', 'Never'],
    'ObjCBlockIndentWidth': ['RANDINT', 1, 20],
    'ObjCBreakBeforeNestedBlockParam': ['BOOL'],
    'ObjCSpaceAfterProperty': ['BOOL'],
    'ObjCSpaceBeforeProtocolList': ['BOOL'],
    'PPIndentWidth': ['RANDINT', 1, 20],
    'PackConstructorInitializers': ['Never', 'BinPack', 'CurrentLine', 'NextLine'],
    'PointerAlignment': ['Left', 'Right', 'Middle'],
    'ReferenceAlignment': ['Left', 'Right', 'Middle'],
    'ReflowComments': ['BOOL'],
    'ShortNamespaceLines': ['RANDINT', 1, 20],
    'SpaceAfterCStyleCast': ['BOOL'],
    'SpaceAfterLogicalNot': ['BOOL'],
    'SpaceAfterTemplateKeyword': ['BOOL'],
    'SpaceAroundPointerQualifiers': ['Default', 'Before', 'After', 'Both'],
    'SpaceBeforeAssignmentOperators': ['BOOL'],
    'SpaceBeforeCaseColon': ['BOOL'],
    'SpaceBeforeCpp11BracedList': ['BOOL'],
    'SpaceBeforeCtorInitializerColon': ['BOOL'],
    'SpaceBeforeInheritanceColon': ['BOOL'],
    'SpaceBeforeParens': ['Never', 'ControlStatements', 'ControlStatementsExceptControlMacros', 'NonEmptyParentheses', 'Always'],
    'SpaceBeforeRangeBasedForLoopColon': ['BOOL'],
    'SpaceBeforeSquareBrackets': ['BOOL'],
    'SpaceInEmptyBlock ': ['BOOL'],
    'SpaceInEmptyParentheses': ['BOOL'],
    'SpacesBeforeTrailingComments': ['RANDINT', 0, 20],
    'SpacesInAngles': ['Never', 'Always'],
    'SpacesInCStyleCastParentheses': ['BOOL'],
    'SpacesInConditionalStatement': ['BOOL'],
    'SpacesInContainerLiterals': ['BOOL'],
    #'SpacesInLineCommentPrefix': ['RANDINT', -1, 1],
    'SpacesInParentheses': ['BOOL'],
    'SpacesInSquareBrackets': ['BOOL'],
    'TabWidth': ['RANDINT', 0, 20],
    'UseTab': ['Never', 'ForIndentation', 'ForContinuationAndIndentation', 'AlignWithSpaces', 'Always']
}


def rand_bool():
    return random.choice(['true', 'false'])


def create_config():
    config = {}
    for option, value in options.items():
        if option == 'BraceWrapping':
            config[option] = {}
            for sub_value in options['BraceWrapping']:
                if value[sub_value][0] == 'BOOL':
                    config[option][sub_value] = rand_bool()
                else:
                    config[option][sub_value] = random.choice(value[sub_value])
        elif value[0] == 'BOOL':
            config[option] = rand_bool()
        elif value[0] == 'RANDINT':
            config[option] = random.randint(value[1], value[2])
        else:
            config[option] = random.choice(value)
    return str(config).replace("'", "")


# Stolen from https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python/68385697#68385697
def count_lines(fname):
    def _make_gen(reader):
        b = reader(2 ** 16)
        while b:
            yield b
            b = reader(2 ** 16)

    with open(fname, "rb") as f:
        count = sum(buf.count(b"\n") for buf in _make_gen(f.raw.read))
    return count


def main(input_file):
    total_lines = count_lines(input_file)
    cmd = ['clang-format', '-i', '--style=', '--lines=', input_file]
    pbar = tqdm(total=total_lines, desc="Ruining file...", unit='ln')

    line = 1
    while line <= total_lines:
        cmd[2] = f'--style={create_config()}'
        cmd[3] = f'--lines={line}:{line}'
        subprocess.Popen(cmd)
        total_lines = count_lines(input_file)
        pbar.total = total_lines
        pbar.refresh()
        pbar.update(1)
        if line >= total_lines:
            break
        line += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The terrible clang-format randomizer')
    parser.add_argument('input_file')
    args = parser.parse_args()
    main(args.input_file)
