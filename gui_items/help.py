class HelpHandler:
    def __init__(self, centertext, dropzones, handzone, drawzone, discardzone):
        self.mode = 0
        self.center_text = centertext
        self.drawzone = drawzone
        self.dropzones = dropzones
        self.handzone = handzone
        self.discardzone = discardzone
        self.help_fns = [self.mode_zero, self.mode_one, self.mode_two, self.mode_three, self.mode_four]
        
    def advance(self):
        self.mode = (self.mode + 1) % 5
        (self.help_fns[self.mode])()
        
        
    def mode_zero(self):
        self.discardzone.set_help(False)
        self.center_text.change_msg("Press H for help, R to restart")
        
    def mode_one(self):
        self.drawzone.set_help(True)
        self.center_text.change_msg("Welcome to ALTAR! Click here to draw a card from the deck (press H to continue)")
        
    def mode_two(self):
        self.drawzone.set_help(False)
        for dropzone in self.dropzones:
            dropzone.set_help(True)
            
        self.center_text.change_msg("With a card held by the mouse, click to place a card in one of these spaces to see its effects.  Right click on a card sitting in one of these spaces to reapply it (press H to continue)")

        
    def mode_three(self):
        for dropzone in self.dropzones:
                dropzone.set_help(False)
        self.handzone.set_help(True)
        self.center_text.change_msg("Place a card in your \"hand\" here for storage for later.  You can freely move cards between your hand and any of the above spaces (press H to continue)")
        
    def mode_four(self):
        self.handzone.set_help(False)
        self.discardzone.set_help(True)
        self.center_text.change_msg("Place a card here to remove it.  Discarding all cards will end the game (press H to finish tutorial)")