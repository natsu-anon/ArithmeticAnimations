((nil . ((eval . (defun prepare-addon ()
				   ;; prepare the pies
				   (interactive)
				   (async-shell-command "powershell.exe d:/Repos/ArithmeticAnimations/prep.ps1")))))
 (python-mode . ((eval . (add-hook 'after-save-hook #'prepare-addon))))
)
