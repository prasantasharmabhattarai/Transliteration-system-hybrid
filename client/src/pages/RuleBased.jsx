import { useState } from 'react';
import axios from 'axios';
import Sidebar, { SidebarItem } from '../components/Sidebar';
import { HomeIcon, UsersIcon } from 'lucide-react';

export default function RuleBased() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [categories, setCategories] = useState({
    independent_vowels: [],
    consonants: [],
    dependent_vowels: [],
    digits: [],
    symbols: [],
    punctuation: []
  });

  const handleChange = (e) => {
    setInput(e.target.value);
  };

  const submitclick = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`http://127.0.0.1:8000/transliterate_rule`, { text: input });
      setOutput(response.data.ans);
      setCategories({
        independent_vowels: response.data.independent_vowels,
        consonants: response.data.consonants,
        dependent_vowels: response.data.dependent_vowels,
        digits: response.data.digits,
        spaces: response.data.spaces,
        symbols: response.data.symbols,
        punctuation: response.data.punctuation
      });
    } catch (error) {
      console.error("Error occurred while transliterating:", error);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      {/* Sidebar - fixed width */}
      <div className="h-full">
        <Sidebar>
          <SidebarItem icon={<HomeIcon />} text="Pure Rule Based" to="/" />
          <SidebarItem icon={<UsersIcon />} text="Statistical Approach" to="/statistical" />
        </Sidebar>
      </div>

      {/* Main content - takes full remaining width */}
      <div className="flex-1 overflow-auto p-6 bg-gray-100">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-3xl font-bold text-center mb-6">
            Transliteration System For Pracalit Script
          </h1>

          <form onSubmit={submitclick} className="space-y-6">
            <div>
              <label htmlFor="pracalit_text" className="block mb-2 text-lg font-medium text-gray-800">
                Text in Pracalit
              </label>
              <textarea
                id="pracalit_text"
                value={input}
                onChange={handleChange}
                className="bg-white w-full p-3 rounded-lg border border-gray-300 resize-y min-h-[150px]"
                placeholder="Namaste"
              />
            </div>

            <div>
              <label htmlFor="transliterated_text" className="block mb-2 text-lg font-medium text-gray-800">
                Transliterated Text
              </label>
              <textarea
                id="transliterated_text"
                value={output}
                disabled
                className="w-full p-3 rounded-lg border border-gray-300 bg-white resize-y min-h-[150px]"
                placeholder="Result"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-blue-700 text-white p-3 rounded-lg font-semibold hover:bg-blue-800"
            >
              Submit
            </button>
          </form>

          <div className="mt-8 text-sm text-gray-700 space-y-2">
            <div><strong>Independent Vowels:</strong> {categories.independent_vowels.join(', ')}</div>
            <div><strong>Consonants:</strong> {categories.consonants.join(', ')}</div>
            <div><strong>Dependent Vowels:</strong> {categories.dependent_vowels.join(', ')}</div>
            <div><strong>Digits:</strong> {categories.digits.join(', ')}</div>
            <div><strong>Symbols:</strong> {categories.symbols.join(', ')}</div>
            <div><strong>Punctuation:</strong> {categories.punctuation.join(', ')}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
