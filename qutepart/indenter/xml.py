from qutepart.indenter.base import IndenterBase

class IndenterXml(IndenterBase):
    """TODO implement
    """
    def computeIndent(self, block, char):
        """Compute indent for the block
        """
        lineText = block.text()
        prevLineText = self._prevNonEmptyBlock(block).text()
        
        alignOnly = char == ''
        
        if alignOnly:
            # XML might be all in one line, in which case we want to break that up.
            tokens = re.split('>\s*<', lineText)

            if len(tokens) > 1:
                
                prevIndent = self._lineIndent(prevLineText)
                
                for index, newLine in enumerate(tokens):
                    if index > 0:
                        newLine = '<' + newLine
                    
                    if index < len(tokens) - 1:
                        newLine = newLine + '>'
    
                    re.match('^\s*</', newLine):
                        char = '/'
                    elif re.match('\>[^<>]*$', newLine):
                        char = '>'
                    else
                        char = '\n'
                    
                    indentation = self.processChar(newLine, prevLineText, char)
                    newLine = indentation + newLine
                    
                    tokens[index] = newLine
                    prevLineText = newLine;
                
                print '\n'.join(tokens)
                print oldLine
            
                qpart.lines[block.blockNumber()] =  '\n'.join(tokens)
                return prevIndent
            else:  # no tokens, do not split line, just compute indent
                if re.match('^\s*<\/', lineText):
                    char = '/'
                elif re.match('\>[^<>]*', lineText):
                    char = '>'
                else:
                    char = '\n'
    
        return processChar(lineText, prevLineText, char)
    
    def processChar(self, lineText, prevLineText, char):
        prevIndent = self._lineIndent(prevLineText)
        if char == '/':
            if not re.match('^\s*<\/', lineText):
                # might happen when we have something like <foo bar="asdf/ycxv">
                # don't change indentation then
                return prevIndent

            if not re.match('<[^\/][^>]*[^\/]>[^<>]*$', prevLineText):
                # decrease indent when we write </ and prior line did not start a tag
                return self._decreaseIndent(prevIndent)
        elif char == '>':
            # increase indent width when we write <...> or <.../> but not </...>
            # and the prior line didn't close a tag
            if re.match('^<(\?xml|!DOCTYPE)', prevLineText):
                return ''
            elif re.match('^\s*<\/', lineText):
                #closing tag, decrease indentation when previous didn't open a tag
                if re.match('<[^\/][^>]*[^\/]>[^<>]*$', prevLineText):
                    # keep indent when prev line opened a tag
                    return prevIndent;
                else:
                    return self._decreaseIndent(prevIndent)
            elif re.match('<([\/!][^>]+|[^>]+\/)>\s*$', prevLineText):
                # keep indent when prev line closed a tag or was empty or a comment
                return prevIndent
            
            return self._increaseIndent(prevIndent)
        elif char == '\n':
            if re.match('^<(\?xml|!DOCTYPE)', prevLineText):
                return ''
            elif re.match('<[^\/!][^>]*[^\/]>[^<>]*$', prevLineText):
                # increase indent when prev line opened a tag (but not for comments)
                return self._increaseIndent(prevIndent)
    
        return prevIndent
