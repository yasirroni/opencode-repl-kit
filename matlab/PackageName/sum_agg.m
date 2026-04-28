function result = sum_agg(data, column)
    % sum_agg - Sum of values in a column.
    %
    % Args:
    %   data: Numeric array or struct array.
    %   column: Field name (for struct data) or empty (for numeric data).
    %
    % Returns:
    %   Sum of values. 0 if empty.

    if isempty(data)
        result = 0;
        return;
    end

    values = extract_values(data, column);
    values = values(~isnan(values));
    result = sum(values);
end

function values = extract_values(data, column)
    if isstruct(data)
        values = [data.(column)];
    else
        values = data(:)';
    end
end
