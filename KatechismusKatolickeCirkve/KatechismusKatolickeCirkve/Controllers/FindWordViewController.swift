//
//  FindWordViewController.swift
//  KatechismusKatolickeCirkve
//
//  Created by Petr Hracek on 12/09/2018.
//  Copyright © 2018 Petr Hracek. All rights reserved.
//

import UIKit
import Foundation

class FindWordViewController: UIViewController, UITextFieldDelegate {

    @IBOutlet weak var wordTextField: UITextField!
    @IBOutlet weak var labelForNoneResults: UILabel!
    var findWordData = [Int]()
    var findWordString: String = ""
    fileprivate var paragraphStructure: ParagraphStructure?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        paragraphStructure = ParagraphDataService.shared.paragraphStructure
        wordTextField.delegate = self
        wordTextField.returnKeyType = .done
        labelForNoneResults.isEnabled = false
        labelForNoneResults.text = ""
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        super.prepare(for: segue, sender: sender)
        switch(segue.identifier ?? "") {
            
        case "ShowParagraph":
            guard let paragraphTableViewController = segue.destination as? ParagraphTableViewController else {
                fatalError("Unexpected destination: \(segue.destination)")
            }
            paragraphTableViewController.kindOfSource = 2
            paragraphTableViewController.findWordString = self.findWordString
            paragraphTableViewController.findWordData = findWordData
            
        default:
            fatalError("Unexpected Segue Identifier; \(String(describing: segue.identifier))")
        }
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        guard let paragraphStructure = paragraphStructure else { return false}
        self.findWordString = wordTextField.text!
        for par in paragraphStructure.paragraph {
            if par.text_no_html.range(of: findWordString) != nil {
                findWordData.append(par.id)
            }
            if par.caption_no_html.range(of: findWordString) != nil {
                findWordData.append(par.id)
            }
        }
        if findWordData.count != 0 {
            performSegue(withIdentifier: "ShowParagraph", sender: self)
            wordTextField.resignFirstResponder()
        }
        else {
            labelForNoneResults.isEnabled = true
            labelForNoneResults.text = "Hledaný výraz nebyl nalezen"
        }
        return true
    }

}
